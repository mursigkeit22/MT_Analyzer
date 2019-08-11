from nltk import ngrams
n = 4

import re

def log_in_file(text):
    with open('python.log', 'a', encoding='utf-8') as log_file:
        log_file.write(text + '\n')

def marking_indentations(text):
    text = re.sub('\n+', '\n', text)
    list_paragraphs = text.split('\n')
    indentation_marks_list = []
    summ = 0
    for paragraph in list_paragraphs:
        words_in_paragraph = len(paragraph.split())
        indentation_marks_list.append(summ)
        summ += words_in_paragraph
    print('INDENTATION_MARKS_LIST: ', indentation_marks_list)
    log_in_file('1) len(INDENTATION_MARKS_LIST): ' + str(len(indentation_marks_list)))
    return indentation_marks_list


def making_set_of_common_grams(text1, text2):
    text1 = text1.split()
    text2 = text2.split()
    grams1 = ngrams(text1, n)
    set_of_grams1 = set(grams1)
    grams2 = ngrams(text2, n)
    set_of_grams2 = set(grams2)
    set_of_common_grams = set_of_grams1.intersection(set_of_grams2)
    log_in_file('2)LEN(SET_OF_COMMON_GRAMS): ' + str(len(set_of_common_grams)))
    return set_of_common_grams


def making_list_of_reapeated_gramms(text1, text2, set_common_grams):
    grams1 = ngrams(text1.split(), n)
    list_of_grams1 = list(grams1)
    grams2 = ngrams(text2.split(), n)
    list_of_grams2 = list(grams2)
    to_exclude = set()
    for gramm in set_common_grams:
        if list_of_grams1.count(gramm) > 1:
            to_exclude.add(gramm)
        if list_of_grams2.count(gramm) > 1:
            to_exclude.add(gramm)
    log_in_file('3) LEN(list_of_reapeated_gramms): ' + str(len(to_exclude)))
    return to_exclude


def adding_tags(text, set_of_common_grams, set_to_exclude):

    def what_current_ngramm(current_pos, split_text):
        current_ngramm = []
        for i in range(n):
            current_ngramm.append(split_text[current_pos + i])
        current_ngramm = tuple(current_ngramm)
        return current_ngramm

    text_split1 = list(text.split())
    tagged_list = list(text.split())
    start_tag = '<span style="background-color: #afdfe1">'
    end_tag = '</span>'
    for gramm in set_of_common_grams.difference(set_to_exclude):
        current_pos = 0
        current_ngramm = what_current_ngramm(current_pos, text_split1)
        while current_ngramm != gramm and current_pos < len(text.split()) - n:
            current_pos += 1
            current_ngramm = what_current_ngramm(current_pos, text_split1)
        else:
            for i in range(n):
                tagged_list[current_pos + i] = start_tag + text_split1[current_pos + i] + end_tag
    for el in set_to_exclude:
        current_pos = 0
        while current_pos < len(text.split()) - n+1:
            current_ngramm = what_current_ngramm(current_pos, text_split1)
            if el == current_ngramm:
                for i in range(n):
                    tagged_list[current_pos + i] = start_tag + text_split1[current_pos + i] + end_tag
            current_pos += 1
    log_in_file('4) adding_tags is almost done')
    return tagged_list


def calc_percentage(tagged_list_trans):  # после def_with_tags, до placing_indent
    number_words = len(tagged_list_trans)
    number_tags = 0
    for el in tagged_list_trans:
        if '<span style="background-color:' in el:
            number_tags += 1
    res_float = number_tags / number_words
    percentage = int(res_float * 100)
    print('PERCENTAGE: ', percentage)
    log_in_file('5) PERCENTAGE: ' + str(percentage))
    return percentage


def making_paragraphs(indentation_marks_list, tagged_list):
    list_with_tags_and_indents = []
    for j in range(len(indentation_marks_list) - 1):
        for i in range(indentation_marks_list[j], indentation_marks_list[j + 1]):
            list_with_tags_and_indents.append(tagged_list[i])
        list_with_tags_and_indents.append('<br>')
    for i in range(indentation_marks_list[-1], len(tagged_list)):
        list_with_tags_and_indents.append(tagged_list[i])
    log_in_file('6) making_paragraphs is almost done')
    return list_with_tags_and_indents


def colouring_spaces(list_with_tags_and_indents):
    list = list_with_tags_and_indents
    new_list = []
    for i in range(len(list)-1):
        if '<span style="background-color:' in list[i] and '<span style="background-color:' in list[i+1]:
            new_list.append(list[i])
            new_list.append('<span style="background-color: #afdfe1"> </span>')
        else:
            new_list.append(list[i])
            new_list.append(' ')
    new_list.append(list[-1])
    log_in_file('7) colouring_spaces is almost done')
    return new_list


def creating_html(list_with_coloured_spaces1, list_with_coloured_spaces2, filename, directory):
    text_withtags_google = ''.join(list_with_coloured_spaces1)
    text_withtags_trans = ''.join(list_with_coloured_spaces2)
    name_txt = directory + '\\' + str(filename) + '.html'
    with open(name_txt, 'w', encoding='utf-8') as future_html:
        future_html.write("""
        <!DOCTYPE html>
<html lang="">
<head>
    <meta charset="UTF-8">
    <title>""" + filename + """</title>
    <link rel="stylesheet" href="../../style_third_window.css">
</head>
<body>
<table class="table"  >
   <tr>
    <td class="left" valign="top">""" + text_withtags_google + """</td>
    <td class="right" valign="top">""" + text_withtags_trans + """</td>

   </tr>
</table>

</body>
</html>""")
    log_in_file('8) creating_html is done')
