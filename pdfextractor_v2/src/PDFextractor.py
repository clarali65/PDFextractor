import fitz, os,csv
from config import parse_args,keyrequirement

def attach_readin(file):
    doc_attach = fitz.open(file)
    f_out = file.replace('pdf', 'txt')
    out = open(f_out, 'w', encoding='utf-8')
    for page in doc_attach:
        text = page.getText()# iterate the document pages
        out.write(text)  # write text of page
        out.write("\n-----\n")  # write page delimiter
    out.close()

if __name__ == '__main__':
    args = parse_args()

    pdf_path = args.pdf_path
    students_folder = args.student_file_folder
    examiner_folder = args.examiner_folder
    output_csv = args.output_csv

    if not os.path.exists(students_folder):
        os.mkdir(students_folder)
    if not os.path.exists(examiner_folder):
        os.mkdir(examiner_folder)

    writer = csv.writer(open(output_csv, "w", newline=''))
    writer.writerow(keyrequirement)

    for doc_idx, document in enumerate(os.listdir(pdf_path)):
        print('processed pdf files: {}'.format(doc_idx))
        doc = fitz.Document(os.path.join(pdf_path, document))
        doc.authenticate('0000')
        csv_dict = dict()
        i0=i1 = i2 = i3 = i4 = 0
        Student_files_path = []
        Examiner_files_path = []

        for page_idx, page in enumerate(doc):
            annot = page.firstAnnot
            while annot:
                if annot.type[0] == fitz.ANNOT_WIDGET: # process each widget
                    if annot.widget_name in keyrequirement:
                        key = annot.widget_name
                        value = annot.widget_value
                        csv_dict[key] = str(value)
                elif annot.type[0] == fitz.ANNOT_FILEATTACHMENT: # process each attachment
                    fileInfo = annot.fileInfo() # get attachment info
                    fileContent = annot.fileGet() # get attachment content
                    annot_location = tuple(annot.rect)
                    attach_file_name = fileInfo['filename'].lower() # get attachment name
                    if page_idx == 0:
                        i0 += 1
                        f_out_name = os.path.join(students_folder, attach_file_name)
                        modified_name = '_'.join([f_out_name[:-4], str(doc_idx), str(i0),f_out_name[-4:]])
                        Student_files_path.append(modified_name)
                    elif page_idx == 1:
                        if annot_location[3] < 544:
                            i1 += 1
                            Examiner_name_1 = csv_dict['Sup.External_Examiner1(by_Sup)'] + '.pdf'
                            modified_name = os.path.join(examiner_folder, '_'.join([Examiner_name_1,str(i1)])+'.pdf')
                        else:
                            i2 += 1
                            Examiner_name_2 = csv_dict['Sup.External_Examiner2(by_Sup)'] + '.pdf'
                            modified_name = os.path.join(examiner_folder, '_'.join([Examiner_name_2,str(i2)])+'.pdf')
                        Examiner_files_path.append(modified_name)
                    elif page_idx == 3:
                        if annot_location[3] < 372:
                            i3 += 1
                            Examiner_name_1 = csv_dict['External_Examiner1(by_InternalExaminer)'] + '.pdf'
                            modified_name = os.path.join(examiner_folder, '_'.join([Examiner_name_1,str(i3)])+'.pdf')
                        else:
                            i4 += 1
                            Examiner_name_2 = csv_dict['External_Examiner2(by_InternalExaminer)'] + '.pdf'
                            modified_name = os.path.join(examiner_folder, '_'.join([Examiner_name_2,str(i4)])+'.pdf')
                        Examiner_files_path.append(modified_name)
                    else:
                        annot = annot.next
                        continue

                    with open(modified_name, 'wb') as f: # write attachment to the folder
                        f. write(fileContent)
                    attach_readin(modified_name) # convert pdf to txt
                else:
                    annot = annot.next
                    continue

                annot = annot.next

        output_line = []
        csv_dict['Student_files'] = ','.join(Student_files_path)
        csv_dict['Examiner_files'] = ','.join(Examiner_files_path)

        for key in keyrequirement:
            output_line.append(csv_dict[key])

        writer.writerow(output_line)
