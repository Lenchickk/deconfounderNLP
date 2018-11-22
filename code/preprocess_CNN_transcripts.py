import os, string
import re, glob, csv, sys
from nltk import sent_tokenize

output_path = '/home/romina/Documents/work/Speeches_mining/outputs'
input_path = '/home/romina/Documents/work/transcripts_mining/transcripts/CNN'
input_directory = ['Anderson Cooper 360', 'Campbell Brown', 'CNN Live Today', 'CNN News Room', 'CNN Tonight'
    , 'Connie Chung Tonight', 'Crossfire', 'Erin Burnett OutFront', 'Glenn Beck',
                   'Greenfield at Large', 'John King, USA', 'Larry King Live', 'Moneyline and Lou Dobbs Tonight',
                   'News Night with Aaron Brown', 'Parker Spitzer', 'Paul Zahn Now and Live from the Headlines',
                   'Piers Morgan', 'The Point with Greta Van Susteren', 'The Situation Room with Wolf Blitzer',
                   'Wolf Blitzer Reports']


def preprocess():
    csv.field_size_limit(sys.maxsize)
    translator = str.maketrans('', '', string.punctuation)
    # for i in range(len(input_directory)):
    for i in range(1):
        os.chdir(input_path + '/' + input_directory[i])
        date_text = dict()
        for txt_file in glob.glob("*.txt"):
            file = open(txt_file, 'r')
            print(file.name)
            # find year by file name to avoid useless processing
            year = int(re.findall(r'_\d+', file.name)[0][1:])
            if year < 2005 or year > 2012:
                continue
            content = file.read()
            # to split each document : they have this pattern in the first line 1 of 415 DOCUMENTS
            segments = re.split(r'\d+ of \d+ DOCUMENTS', content)[1:]
            count = 0
            for text in segments:
                # first line which the main text starts
                start = text.index('LENGTH') + 6 + 13
                # end of the main text
                end = text.index('LOAD-DATE')
                main_text = text[start:end]
                enter_seperated_line = main_text.split('\n')
                # without_speaker = re.sub(r'([A-Z]+\s*(\((\w|\s)+\))?\s*)+:', ' ', main_text_clean)
                line_without_capital = ''
                for lines in enter_seperated_line:
                    # redundant_details = re.search(r'\(([A-Z]+|\s*)+\)', l)
                    # line= re.sub(' +', ' ', l)
                    # (CAMERA-ON)
                    if lines.isupper():
                        continue
                    all_lines = sent_tokenize(lines)
                    for line in all_lines:
                        # I A DR.
                        if line.isupper():
                            continue
                        speakers = line.split(':')
                        is_speaker = False
                        if len(speakers) > 1:
                            speaker = speakers[0]
                            if speaker.isupper():
                                is_speaker = True
                            else:
                                details_start = speaker.split('(')
                                if (len(details_start) > 1):
                                    details_end = details_start[1].split(')')
                                    if len(details_end) > 1:
                                        speaker = details_start[0] + details_end[1]
                                        if speaker.isupper() or speaker == '':
                                            is_speaker = True
                        if is_speaker:
                            line_without_capital += ''.join(speakers[1:])
                        else:
                            line_without_capital += ' ' + line
                no_punc_text = line_without_capital.translate(translator)
                clean_text = ' '.join(no_punc_text.split())
                # for each date, merge all observations
                if year not in date_text.keys():
                    date_text[year] = clean_text
                else:
                    date_text[year] += clean_text
    return date_text


def write(to_write):
    os.chdir(output_path)
    f = open('CNN_transcripts_by_year_2005_12.csv', 'w')
    w = csv.writer(f)
    w.writerow(['date', 'text'])
    for date, text in to_write.items():
        print(date)
        w.writerow([date, text])


date_text = preprocess()
write(date_text)
