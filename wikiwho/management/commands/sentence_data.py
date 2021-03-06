# -*- coding: utf-8 -*-
"""
Example usage:
python manage.py sentence_data -m 6 -log '/home/kenan/PycharmProjects/wikiwho_api/tmp_pickles' -lang 'en'
"""
import glob
import sys
import json

from os import mkdir
from os.path import join, basename, exists
from time import strftime, sleep
from simplejson import JSONDecodeError
from concurrent.futures import ProcessPoolExecutor, as_completed

from django.utils.dateparse import parse_datetime
from django.core.management.base import BaseCommand

from api.utils_pickles import get_pickle_folder, pickle_load
from base.utils_log import get_logger

# TODO delete assertions


def words(s):
    return [w.value for w in s.words]


def jaccard_similarity(l1, l2):
    intersection = len(set(l1).intersection(l2))
    union = (len(l1) + len(l2)) - intersection
    return intersection/union


def calculate_sentence_similarity(s1, s2):
    t1 = [w.token_id for w in s1.words]
    t2 = [w.token_id for w in s2.words]
    return jaccard_similarity(t1, t2)


def extend_sentence_data(pickle_path):
    retries = 6
    while retries:
        retries -= 1
        try:
            wikiwho = pickle_load(pickle_path)
        except (UnboundLocalError, JSONDecodeError):
            sleep(30)
            if not retries:
                raise
    sentence_id = 0
    all_sentences = {}  # {sentence_id: sentence_obj}
    prev_rev_id = None  # used to find out re-added sentences
    rev_prev_sentence_ids = None  # used to find out deleted sentences
    for rev_id in wikiwho.ordered_revisions:
        rev = wikiwho.revisions[rev_id]
        rev.timestamp = parse_datetime(rev.timestamp)
        rev_sentence_ids = []  # list of sentence ids of this revision in order
        rev_added_sentence_ids = []  # list of (re/new) added sentences in this revision
        tmp = {'p': [], 's': []}  # this is used to get sentences in correct order
        # iterate sentences of this revision in order
        for p_hash in rev.ordered_paragraphs:
            if len(rev.paragraphs[p_hash]) > 1:
                tmp['p'].append(p_hash)
                paragraph = rev.paragraphs[p_hash][tmp['p'].count(p_hash)-1]
            else:
                paragraph = rev.paragraphs[p_hash][0]
            tmp['s'][:] = []
            for s_hash in paragraph.ordered_sentences:
                if len(paragraph.sentences[s_hash]) > 1:
                    tmp['s'].append(s_hash)
                    sentence = paragraph.sentences[s_hash][tmp['s'].count(s_hash)-1]
                else:
                    sentence = paragraph.sentences[s_hash][0]
                # TODO (later) filter sentecse, e.g. <ref ... /fev>
                if not hasattr(sentence, 'ins'):
                    # this is a new added sentence
                    sentence.id_ = sentence_id
                    sentence.ins = [rev_id]
                    sentence.outs = []
                    rev_added_sentence_ids.append(sentence.id_)
                    assert sentence_id not in all_sentences
                    all_sentences.update({sentence_id: sentence})
                    sentence_id += 1
                else:
                    if sentence.last_rev_id != prev_rev_id:
                        # sentence is re-added
                        sentence.ins.append(rev_id)
                        rev_added_sentence_ids.append(sentence.id_)
                sentence.last_rev_id = rev_id
                rev_sentence_ids.append(sentence.id_)
        rev.sentence_ids = rev_sentence_ids
        rev.added_sentence_ids = rev_added_sentence_ids
        # add deletion info to sentences
        if rev_prev_sentence_ids is not None:
            rev.deleted_sentence_ids = list(set(rev_prev_sentence_ids) - set(rev_sentence_ids))
        else:
            rev.deleted_sentence_ids = []
        for s_id in rev.deleted_sentence_ids:
            all_sentences[s_id].outs.append(rev_id)
        rev_prev_sentence_ids = rev_sentence_ids[:]
        prev_rev_id = rev_id
    wikiwho.all_sentences = all_sentences
    return wikiwho


def generate_sentence_data(pickle_path, output_folder):
    ww = extend_sentence_data(pickle_path)
    output = {'title': ww.title,
              'page_id': ww.page_id}
    seconds_limit = 48 * 3600  # hours
    for s_id in range(len(ww.all_sentences)):
        sentence = ww.all_sentences[s_id]
        for i, out_rev_id in enumerate(sentence.outs):
            out_ts = ww.revisions[out_rev_id].timestamp
            in_rev_id = sentence.ins[i]
            in_ts = ww.revisions[in_rev_id].timestamp
            if (out_ts - in_ts).total_seconds() < seconds_limit:
                # unsuccessful
                continue
            # compare this sentence with adds of rev where this sentence is deleted
            for added_s_id in ww.revisions[out_rev_id].added_sentence_ids:
                added_sentence = ww.all_sentences[added_s_id]
                # calculate_sentence_similarity uses token ids to calculate similarity
                # this saves us from matching different but similar sentences,
                # because we get the first match
                if calculate_sentence_similarity(sentence, added_sentence) >= 0.8:
                    x = added_sentence.ins.index(out_rev_id)
                    try:
                        added_out_rev_id = added_sentence.outs[x]
                    except IndexError:
                        pass
                    else:
                        added_in_ts = out_ts
                        added_out_ts = ww.revisions[added_out_rev_id].timestamp
                        if (added_out_ts - added_in_ts).total_seconds() >= seconds_limit:
                            # successful
                            break
                        for added_s_id_2 in ww.revisions[added_out_rev_id].added_sentence_ids:
                            added_sentence_2 = ww.all_sentences[added_s_id_2]
                            if calculate_sentence_similarity(added_sentence, added_sentence_2) >= 0.8:
                                x = added_sentence_2.ins.index(added_out_rev_id)
                                try:
                                    added_out_rev_id_2 = added_sentence_2.outs[x]
                                except IndexError:
                                    pass
                                else:
                                    added_in_ts_2 = added_out_ts
                                    added_out_ts_2 = ww.revisions[added_out_rev_id_2].timestamp
                                    if (added_out_ts_2 - added_in_ts_2).total_seconds() >= seconds_limit:
                                        # successful
                                        sr_id = '{}-{}'.format(s_id, in_rev_id)
                                        assert sr_id not in output
                                        output[sr_id] = {
                                            's_id': s_id,
                                            'tokens': [t.value for t in sentence.words],
                                            'in_rev_id': in_rev_id,
                                            'in_rev_ts': in_ts,
                                            'deleted': {
                                                's_id': added_s_id,
                                                'tokens': [t.value for t in added_sentence.words],
                                                'in_rev_id': out_rev_id,
                                                'in_rev_ts': out_ts,
                                                'deleted': {
                                                    's_id': added_s_id_2,
                                                    'tokens': [t.value for t in added_sentence_2.words],
                                                    'in_rev_id': added_out_rev_id,
                                                    'in_rev_ts': added_out_ts,
                                                    'deleted': {
                                                        'in_rev_id': added_out_rev_id_2,
                                                        'in_rev_ts': added_out_ts_2,
                                                    }
                                                }
                                            }
                                        }
                    break

    with open(join(output_folder, '{}.json'.format(ww.page_id)), 'w') as fp:
        json.dump(output, fp, default=str)
    ww.output = output
    return ww


def generate_sentence_data_base(pickle_path, output_folder):
    ww = generate_sentence_data(pickle_path, output_folder)
    return ww.page_id


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', required=False,
                            help='Pickles json file {"en": [list of page ids], "de" [], }. '
                                 'If not given, list is taken from relevant pickle folder for each language.')
        parser.add_argument('-lang', '--language', help="Wikipedia language. Ex: 'en' or 'en,eu,de'", required=True)
        parser.add_argument('-log', '--log_folder', help='Folder where to write logs.', required=True)
        parser.add_argument('-m', '--max_workers', type=int, help='Number of processors/threads to run parallel. ',
                            required=True)

    def get_parameters(self, options):
        json_file = options['file'] or None
        languages = options['language'].split(',')
        max_workers = options['max_workers']
        return json_file, languages, max_workers

    def handle(self, *args, **options):
        json_file, languages, max_workers = self.get_parameters(options)

        print('Start at {}'.format(strftime('%H:%M:%S %d-%m-%Y')))
        print(max_workers, languages)
        # Concurrent process of pickles of each language to generate editor data
        for language in languages:
            # set logging
            log_folder = options['log_folder']
            if not exists(log_folder):
                mkdir(log_folder)
            logger = get_logger('sentence_data_{}'.format(language),
                                log_folder, is_process=True, is_set=True, language=language)
            pickle_folder = get_pickle_folder(language)
            print('Start: {} - {} at {}'.format(language, pickle_folder, strftime('%H:%M:%S %d-%m-%Y')))

            if json_file:
                with open(json_file, 'r') as f:
                    pickles_dict = json.loads(f.read())
                    pickles_list = [join(pickle_folder, '{}.p'.format(page_id)) for page_id in pickles_dict[language]]
            else:
                pickles_list = list(glob.iglob(join(pickle_folder, '*.p')))
            pickles_all = len(pickles_list)
            pickles_left = pickles_all
            pickles_iter = iter(pickles_list)
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                jobs = {}
                while pickles_left:
                    for pickle_path in pickles_iter:
                        page_id = basename(pickle_path)[:-2]
                        job = executor.submit(generate_sentence_data_base, pickle_path, log_folder)
                        jobs[job] = page_id
                        if len(jobs) == max_workers:  # limit # jobs with max_workers
                            break

                    for job in as_completed(jobs):
                        pickles_left -= 1
                        page_id_ = jobs[job]
                        try:
                            data = job.result()
                        except Exception as exc:
                            logger.exception('{}-{}'.format(page_id_, language))

                        del jobs[job]
                        sys.stdout.write('\rPickles left: {} - Pickles processed: {:.3f}%'.
                                         format(pickles_left, ((pickles_all - pickles_left) * 100) / pickles_all))
                        break  # to add a new job, if there is any
            print('\nDone: {} - {} at {}'.format(language, pickle_folder, strftime('%H:%M:%S %d-%m-%Y')))
        print('Done at {}'.format(strftime('%H:%M:%S %d-%m-%Y')))
