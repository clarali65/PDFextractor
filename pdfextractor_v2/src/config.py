import argparse

def parse_args():

    parser = argparse.ArgumentParser(description="PDFextractor")

    parser.add_argument('--pdf_path', type=str, default='test_file', help='The name of pdf folder')

    parser.add_argument('--student_file_folder', type=str, default='student_folder', help='The name of student data folder')

    parser.add_argument('--examiner_folder', type=str, default='examiner_folder', help='The name of examiner data folder')

    parser.add_argument('--output_csv', type=str, default='test.csv', help='The name of generated csv')

    return parser.parse_args()

keyrequirement = [
      'Title of Thesis',
      'Area of Research',
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
      'External_Examiner1_Salutation(by_InternalExaminer)',
      'External_Examiner1(by_InternalExaminer)',
      'External_Examiner1_Salutation/Univ_name(by_InternalExaminer)',
      'External_Examiner1_Salutation/Univ_Addr(by_InternalExaminer)',
      'External_Examiner1_Qualifications(by_InternalExaminer)',
      'External_Examiner1_Tel(by_InternalExaminer)',
      'External_Examiner1_EmailAddr(by_InternalExaminer)',
      'External_Examiner2_Salutation(by_InternalExaminer)!',
      'External_Examiner2(by_InternalExaminer)',
      'External_Examiner2_Salutation/Univ_name(by_InternalExaminer)',
      'External_Examiner2_Salutation/Univ_Addr(by_InternalExaminer)',
      'External_Examiner2_Qualifications(by_InternalExaminer)',
      'External_Examiner2_Tel(by_InternalExaminer)',
      'External_Examiner2_EmailAddr(by_InternalExaminer)',
      'Student_files',
      'Examiner_files'
]

