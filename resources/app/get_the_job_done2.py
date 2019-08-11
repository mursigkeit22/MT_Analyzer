import sys
import pythone_functions2 as pf
import docx2txt
text_from_google = sys.argv[-2]
directory = sys.argv[-1]
pf.log_in_file('1. got argv')
pf.log_in_file('DIRECTORY: ' + directory)
current_path = directory + '\\text_second_window.txt'
pf.log_in_file('1.1. CURRENT PATH: ' + current_path)

words_in_text_from_google = len(list(text_from_google.split()))
print('LEN_GOOGLETEXT: ', words_in_text_from_google, ' WORDS')
names_and_paths = dict()  # имя файла: путь до файла
filenames_and_texts = dict()  # имя файла: текст файла
filenames_and_indents = dict()
filenames_and_commongrams = dict()  # имя файла: общие 4-граммы с text_from_google

for i in range(1, len(sys.argv) - 2, 2):
    names_and_paths[sys.argv[i]] = sys.argv[i + 1]
pf.log_in_file('2. LEN(NAMES AND PATHS.DICT): ' + str(len(names_and_paths)))
for name, path in names_and_paths.items():
    filenames_and_texts[name] = docx2txt.process(path)
pf.log_in_file('3. LEN(MADE FILENAMES AND TEXTS.DICT): ' + str(len(filenames_and_texts)))
for name, text in filenames_and_texts.items():
    filenames_and_indents[name] = pf.marking_indentations(filenames_and_texts[name])
pf.log_in_file('4. LEN(FILENAMES AND INDENTS.DICT): ' + str(len(filenames_and_indents)))
for filename, text in filenames_and_texts.items():
    filenames_and_commongrams[filename] = pf.making_set_of_common_grams(text_from_google, text)
pf.log_in_file('5. LEN(FILENAMES AND COMMONGRAMS.DICT): ' + str(len(filenames_and_commongrams)))
with open(current_path, 'w', encoding='utf-8') as made_file:
    made_file.write('<!DOCTYPE html> <html> <head> <meta charset="UTF-8"> '
                    '<title> Results </title> '
                    '<link rel="stylesheet" href="../../style_second_window.css">'

                    ' </head>  <body style="background-color: #afdfe1">'
                    '<table class="table"  > <thead>'
                    '<tr>    <td class="fc-header">File name ⇅</td>'
    '<td class="sc-header">Result ⇅</td>'
       '<td class="tc-header"> </td>'
   '</tr> </thead>    <tbody>')
pf.log_in_file('6. wrote first part of text_second_window.txt')
for filename in filenames_and_texts:

    set_to_exclude = pf.making_list_of_reapeated_gramms(text_from_google, filenames_and_texts[filename],
                                                        filenames_and_commongrams[filename])
    tagged_list_google = pf.adding_tags(text_from_google, filenames_and_commongrams[filename], set_to_exclude)
    tagged_list_trans = pf.adding_tags(filenames_and_texts[filename], filenames_and_commongrams[filename],
                                       set_to_exclude)
    list_with_tags_and_indents_google = pf.making_paragraphs(pf.marking_indentations(text_from_google),
                                                             tagged_list_google)
    list_with_tags_and_indents_trans = pf.making_paragraphs(filenames_and_indents[filename], tagged_list_trans)
    list_with_coloured_spaces_google = pf.colouring_spaces(list_with_tags_and_indents_google)
    list_with_coloured_spaces_trans = pf.colouring_spaces(list_with_tags_and_indents_trans)

    pf.creating_html(list_with_coloured_spaces_google, list_with_coloured_spaces_trans, filename, directory)
    identical_to_write = str(pf.calc_percentage(tagged_list_trans))
    with open(current_path, 'a', encoding='utf-8') as made_file:
        made_file.write('<tr>    <td class="first-column" >' + filename + '</td>    <td class="second-column">' + str(identical_to_write) +
                        """% identical </td>
       <td class="third-column"><button class="button" onclick="window.open('"""
                        + filename + """.html', '', 'width=1200')">open</button></td>
  </tr>""")
    pf.log_in_file('ONE LOOP ENDED')
pf.log_in_file('7. cycle ended')
with open(current_path, 'a', encoding='utf-8') as made_file:
    made_file.write("""</tbody> </table> <script>
    document.addEventListener('DOMContentLoaded', () => {

        const getSort = ({ target }) => {
            const order = (target.dataset.order = -(target.dataset.order || -1));
            const index = [...target.parentNode.cells].indexOf(target);
            const collator = new Intl.Collator(['en', 'ru'], { numeric: true });
            const comparator = (index, order) => (a, b) => order * collator.compare(
                a.children[index].innerHTML,
                b.children[index].innerHTML
            );

            for(const tBody of target.closest('table').tBodies)
                tBody.append(...[...tBody.rows].sort(comparator(index, order)));

            for(const cell of target.parentNode.cells)
                cell.classList.toggle('sorted', cell === target);
        };

        document.querySelectorAll('.table thead').forEach(tableTH => tableTH.addEventListener('click', () => getSort(event)));

    });

</script> </body> </html>""")

pf.log_in_file('8. finished writing to the file')
# results:
print('len and type sys.argv ', len(sys.argv), type(sys.argv))
print('len names_and_paths ', len(names_and_paths))
print('len filenames_and_texts ', len(filenames_and_texts))
pf.log_in_file('9. get_the_job_done2 is finished, FILENAMES: ' + str(list(names_and_paths.keys())))

