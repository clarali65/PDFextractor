import fitz
import csv
import os
pdf_path = "C:/PDFextractor/test_file"
pdfs = os.listdir(pdf_path)
from operator import itemgetter
from itertools import groupby

def ParseTab(page, bbox, columns=None):
    ''' Returns the parsed table of a page in a PDF / (open) XPS / EPUB document.
    Parameters:
    page: fitz.Page object
    bbox: containing rectangle, list of numbers [xmin, ymin, xmax, ymax]
    columns: optional list of column coordinates. If None, columns are generated
    Returns the parsed table as a list of lists of strings.
    The number of rows is determined automatically
    from parsing the specified rectangle.
    '''
    tab_rect = fitz.Rect(bbox).irect
    xmin, ymin, xmax, ymax = tuple(tab_rect)

    if tab_rect.isEmpty or tab_rect.isInfinite:
        print("Warning: incorrect rectangle coordinates!")
        return []

    if type(columns) is not list or columns == []:
        coltab = [tab_rect.x0, tab_rect.x1]
    else:
        coltab = sorted(columns)

    if xmin < min(coltab):
        coltab.insert(0, xmin)
    if xmax > coltab[-1]:
        coltab.append(xmax)

    words = page.getTextWords()

    if words == []:
        print("Warning: page contains no text")
        return []

    alltxt = []

    # get words contained in table rectangle and distribute them into columns
    for w in words:
        ir = fitz.Rect(w[:4]).irect  # word rectangle
        if ir in tab_rect:
            cnr = 0  # column index
            for i in range(1, len(coltab)):  # loop over column coordinates
                if ir.x0 < coltab[i]:  # word start left of column border
                    cnr = i - 1
                    break
            alltxt.append([ir.x0, ir.y0, ir.x1, cnr, w[4]])

    if alltxt == []:
        print("Warning: no text found in rectangle!")
        return []

    # alltxt.sort(key=itemgetter(1))  # sort words vertically

    # create the table / matrix
    spantab = []  # the output matrix

    for y, zeile in groupby(alltxt, itemgetter(1)):
        schema = [""] * (len(coltab) - 1)
        for c, words in groupby(zeile, itemgetter(3)):
            entry = " ".join([w[4] for w in words])
            schema[c] = entry
        spantab.append(schema)

    return spantab

f = open("test.csv","w",newline='')
writer = csv.writer(f)
keyrequirement = ['Title of Thesis', 'Area of Research',
                  'Sup.External_Examiner1_Salutation(by_Sup)',
                  'Sup.External_Examiner1(by_Sup)',
                  'Sup.External_Examiner1_Salutation/Univ_name (by Sup)',
                  'Sup.External_Examiner1_Qualifications(by_Sup)',
                  'Sup.External_Examiner1_Tel(by_Sup)',
                  'Sup.External_Examiner1_EmailAddr(by_Sup)',
                  'Sup.External_Examiner2_Salutation(by_Sup)',
                  'Sup.External_Examiner2(by_Sup)',
                  'Sup.External_Examiner2_Salutation/Univ_name (by Sup)',
                  'Sup.External_Examiner2_Qualifications(by_Sup)',
                  'Sup.External_Examiner2_Tel(by_Sup)',
                  'Sup.External_Examiner2_EmailAddr(by_Sup)',
                  ]
writer.writerow(keyrequirement)
for document in pdfs:
    doc = fitz.Document(os.path.join(pdf_path,document))
    doc.authenticate('0000')
    stu_dic = dict()
    for page in doc:
        annot = page.firstAnnot
        while annot:
            if annot.type[0] != fitz.ANNOT_WIDGET:  # form field type is (19, 'Widget')
                annot = annot.next  # last annot has no "next"
                continue
            try:
                a = annot.widget_text
                print('key:{}'.format(annot.widget_name))
                print('text:{}'.format(annot.widget_text))
                if annot.widget_name in keyrequirement:
                    key = annot.widget_name
                    value = annot.widget_value
                    stu_dic[key] = str(value)
            except:
                print('key:{}'.format(annot.widget_name))
                print('value:{}'.format(annot.widget_value))
                if annot.widget_name in keyrequirement:
                    key = annot.widget_name
                    value = annot.widget_value
                    stu_dic[key] = str(value)
            annot = annot.next

    list_3 = []
    for i in keyrequirement:
        list_3.append(stu_dic[i])

    writer.writerow(list_3)


    list_3 = []
    fin_dic = dict()
    fin_dic = stu_dic.copy()
    fin_dic.update(attach_dic)

    for i in list_2:
        list_3.append(fin_dic[i])

    writer.writerow(list_3)