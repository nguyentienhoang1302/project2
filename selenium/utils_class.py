import time
import io
import os
import random
import requests
import json
import re

list_first_name_vi = ["An", "Uc", "Uat", "Dam", "Dao", "Dinh", "Doan", "An", "Banh", "Bach", "Cao", "Chau", "Chu",
                      "Chu", "Chung", "Duu", "Diep", "Doan", "Giang", "Ha", "Han", "Kieu", "Kim", "Lam", "Luong", "Luu",
                      "Lac", "Luc", "La", "Lieu", "Ma", "Mac", "Mach", "Mai", "Ngu", "Nghiem", "Phi", "Pho", "Phung",
                      "Quach", "Quang", "Quyen", "To", "Ton", "Ta", "Tong", "Thai", "Sai", "Than", "Thach", "Thao",
                      "Thuy", "Thi", "Tieu", "Truong", "Tram", "Trinh", "Trang", "Trieu", "Van", "Vinh", "Vuong", "Vuu",
                      "Nguyen", "Tran", "Le", "Pham", "Huynh", "Hoang", "Phan", "Vu", "Vo", "Dang", "Bui", "Do", "Ho",
                      "Ngo", "Duong", "Ly", "Nguyen", "Tran", "Le", "Pham", "Huynh", "Hoang", "Phan", "Vu", "Vo",
                      "Dang", "Bui", "Do", "Ho", "Ngo", "Duong", "Ly", "Nguyen", "Nguyen", "Nguyen", "Nguyen", "Nguyen",
                      "Nguyen", "Nguyen", "Nguyen", "Nguyen", "Nguyen", "Nguyen", "Nguyen", "Nguyen", "Nguyen",
                      "Nguyen", "Nguyen", "Nguyen", "Tran", "Le", "Pham", "Huynh", "Hoang", "Phan", "Vu", "Vo", "Dang",
                      "Bui", "Do", "Ho", "Ngo", "Duong", "Ly", "Nguyen", "Tran", "Le", "Pham", "Huynh", "Hoang", "Phan",
                      "Vu", "Vo", "Dang", "Bui", "Do", "Ho", "Ngo", "Duong", "Ly"]
list_last_name_vi = ["Bao An", "Binh An", "Dang An", "Duy An", "Khanh An", "Nam An", "Phuoc An", "Thanh An", "The An",
                     "Thien An", "Truong An", "Viet An", "Xuan An", "Cong An", "Duc An", "Gia An", "Hoang An",
                     "Minh An", "Phu An", "Thanh An", "Thien An", "Thien An", "Vinh An", "Ngoc An", "Chi Anh",
                     "Duc Anh", "Duong Anh", "Gia Anh", "Hung Anh", "Huy Anh", "Minh Anh", "Quang Anh", "Quoc Anh",
                     "The Anh", "Thieu Anh", "Thuan Anh", "Trung Anh", "Tuan Anh", "Tung Anh", "Tuong Anh", "Viet Anh",
                     "Vu Anh", "Ho Bac", "Hoai Bac", "Gia Bach", "Cong Bang", "Duc Bang", "Hai Bang", "Yen Bang",
                     "Chi Bao", "Duc Bao", "Duy Bao", "Gia Bao", "Huu Bao", "Nguyen Bao", "Quoc Bao", "Thieu Bao",
                     "Tieu Bao", "Duc Binh", "Gia Binh", "Hai Binh", "Hoa Binh", "Huu Binh", "Khanh Binh", "Kien Binh",
                     "Kien Binh", "Phu Binh", "Quoc Binh", "Tan Binh", "Tat Binh", "Thai Binh", "The Binh", "Xuan Binh",
                     "Yen Binh", "Quang Buu", "Thien Buu", "Khai Ca", "Gia Can", "Duy Can", "Gia Can", "Huu Canh",
                     "Gia Canh", "Huu Canh", "Minh Canh", "Ngoc Canh", "Duc Cao", "Xuan Cao", "Bao Chan", "Bao Chau",
                     "Huu Chau", "Phong Chau", "Thanh Chau", "Tuan Chau", "Tung Chau", "Dinh Chien", "Manh Chien",
                     "Minh Chien", "Huu Chien", "Huy Chieu", "Truong Chinh", "Duc Chinh", "Trong Chinh", "Trung Chinh",
                     "Viet Chinh", "Dinh Chuong", "Tuan Chuong", "Minh Chuyen", "An Co", "Chi Cong", "Thanh Cong",
                     "Xuan Cung", "Huu Cuong", "Manh Cuong", "Duy Cuong", "Viet Cuong", "Ba Cuong", "Duc Cuong",
                     "Dinh Cuong", "Duy Cuong", "Hung Cuong", "Huu Cuong", "Kien Cuong", "Manh Cuong", "Ngoc Cuong",
                     "Phi Cuong", "Phuc Cuong", "Thinh Cuong", "Viet Cuong", "Ngoc Dai", "Quoc Dai", "Minh Dan",
                     "The Dan", "Minh Dan", "Nguyen Dan", "Sy Dan", "Hai Dang", "Hong Dang", "Minh Danh", "Ngoc Danh",
                     "Quang Danh", "Thanh Danh", "Hung Dao", "Thanh Dao", "Binh Dat", "Dang Dat", "Huu Dat", "Minh Dat",
                     "Quang Dat", "Quang Dat", "Thanh Dat", "Dac Di", "Phuc Dien", "Quoc Dien", "Phi Diep", "Dinh Dieu",
                     "Vinh Dieu", "Manh Dinh", "Bao Dinh", "Huu Dinh", "Ngoc Doan", "Thanh Doan", "Thanh Doanh",
                     "The Doanh", "Dinh Don", "Quang Dong", "Tu Dong", "Vien Dong", "Lam Dong", "Bach Du", "Thuy Du",
                     "Hong Duc", "Anh Duc", "Gia Duc", "Kien Duc", "Minh Duc", "Quang Duc", "Tai Duc", "Thai Duc",
                     "Thien Duc", "Thien Duc", "Tien Duc", "Trung Duc", "Tuan Duc", "Hoang Due", "Anh Dung", "Chi Dung",
                     "Hoang Dung", "Hung Dung", "Lam Dung", "Manh Dung", "Minh Dung", "Nghia Dung", "Ngoc Dung",
                     "Nhat Dung", "Quang Dung", "Tan Dung", "The Dung", "Thien Dung", "Tien Dung", "Tri Dung",
                     "Trong Dung", "Trung Dung", "Tuan Dung", "Viet Dung", "Hieu Dung", "Dai Duong", "Dinh Duong",
                     "Dong Duong", "Hai Duong", "Nam Duong", "Quang Duong", "Thai Duong", "Viet Duong", "Anh Duy",
                     "Bao Duy", "Duc Duy", "Khac Duy", "Khanh Duy", "Nhat Duy", "Phuc Duy", "Thai Duy", "Trong Duy",
                     "Viet Duy", "The Duyet", "Vuong Gia", "Bao Giang", "Chi Giang", "Cong Giang", "Duc Giang",
                     "Hai Giang", "Hoa Giang", "Hoang Giang", "Hong Giang", "Khanh Giang", "Long Giang", "Minh Giang",
                     "Thien Giang", "Truong Giang", "Nguyen Giap", "Huy Kha", "Anh Khai", "Duc Khai", "Hoang Khai"]

list_first_name_en = ['Boris', 'Fred', 'Albert', 'Tom', 'James', 'Matthew', 'Mark', 'Luke', 'John', 'David', 'Harold',
                      'Bob', 'Jack', 'Mike', 'Raymond', 'Cuthbert', 'Casper', 'Harry', 'Cameron', 'Warwick', 'Steve',
                      'Steven', 'Simon', 'Jeff', 'Zach', 'Chris', 'Christian', 'Matt', 'Mathias', 'Alex', 'Will',
                      'William', 'Forest', 'Clarke', 'Gregory', 'Joshua', 'Josh', 'Andy', 'Andrew', 'Dick', 'Rick',
                      'Richard', 'Rob', 'Robert', 'Mohammad', 'Hector', 'Reginald', 'Phillip', 'Phil', 'Pete', 'Roger',
                      'Brad', 'Chad', 'Shane', 'Daniel', 'Dan', 'Tristan', 'Roy', 'Gary', 'Tony', 'Toby', 'Barry',
                      'Graham', 'Kevin', 'Tommy', 'Sandie', 'Darth', 'Garth', 'Annie', 'Mary', 'Sarah', 'Laura',
                      'Lauren', 'Katy', 'Kate', 'Catherine', 'Naomi', 'Helen', 'Nadine', 'Alice', 'Alison', 'Susan',
                      'Suzanne', 'Sharon', 'Georgina', 'Sonya', 'Marion', 'Beth', 'Una', 'Sophia', 'Rachel',
                      'Christiana', 'Maud', 'Mildred', 'Zoe', 'Chantal', 'Charlotte', 'Chloe', 'Flora', 'Annabelle',
                      'Elizabeth', 'Morwenna', 'Jenna', 'Jenny', 'Gemma', 'Wenna', 'Fairydust', 'Charity', 'Ocean',
                      'Virginia', 'Hannah', 'Mavis', 'Harriet', 'Kathy', 'Heather', 'Kimberly', 'May', 'Carla', 'Suki',
                      'Michelle', 'Rhiannon', 'Ruth', 'Polly', 'Sally', 'Molly', 'Dolly', 'Maureen', 'Maud', 'Doris',
                      'Felicity', 'Jessica', 'Stanley']
list_last_name_en = ['Gump', 'Doop', 'Gloop', 'Snozcumber', 'Giantbulb', 'Slaughterhouse', 'Godfrey', 'Smith', 'Jones',
                     'Bogtrotter', 'Ramsbottom', 'Cockle', 'Hemingway', 'Pigeon', 'Parker', 'Nolan', 'Parkes',
                     'Butterscotch', 'Barker', 'Trescothik', 'Superhalk', 'Barlow', 'MacDonald', 'Ferguson',
                     'Donaldson', 'Platt', 'Bishop', 'Blunder', 'Thunder', 'Sparkle', 'Walker', 'Raymond', 'Thornhill',
                     'Sweet', 'Parker', 'Johnson', 'Randall', 'Zeus', 'England', 'Smart', 'Gobble', 'Clifford',
                     'Thornton', 'Cox', 'Blast', 'Plumb', 'Wishmonger', 'Fish', 'Blacksmith', 'Thomas', 'Grey',
                     'Russell', 'Lakeman', 'Ball', 'Chan', 'Chen', 'Wu', 'Khan', 'Meadows', 'Connor', 'Williams',
                     'Wilson', 'Blackman', 'Jones', 'Humble', 'Noris', 'Bond', 'Rabbit', 'McCallister', 'DeVito',
                     'Malkovich', 'Olsson', 'Sparrow', 'Kowalski', 'Vader', 'Torrance', 'Greenway', 'Rockatansky',
                     'Pitt', 'Willis', 'Jolie']


class File_Interact():
    def __init__(self, file_name):
        self.file_name = file_name

    def write_file(self, ndung):
        f = io.open(self.file_name, 'w', encoding='utf-8')
        f.write(ndung)
        f.close()

    def write_file_from_list(self, list_lines):
        f = io.open(self.file_name, 'a', encoding='utf-8')
        f.write('\n'.join(list_lines))
        f.close()

    def replace_line_in_file(self, i_line, new_line):
        L = self.read_file_list()
        L2 = L.copy()
        L2[i_line] = new_line
        self.write_file_from_list(L2)

    def write_file_line(self, ndung_line):
        f = io.open(self.file_name, 'a', encoding='utf-8')
        f.write('%s\n' % ndung_line)
        f.close()

    def read_file(self):
        f = io.open(self.file_name, 'r', encoding='utf-8')
        ndung = f.read()
        f.close()
        return ndung

    def read_file_list(self):
        f = io.open(self.file_name, 'r', encoding='utf-8')
        ndung = f.read()
        f.close()
        return ndung.split('\n')


class String_Interact():
    def __init__(self):
        pass

    def regex_one_value(self, pattern, input_str):
        regex1 = re.compile(pattern)
        kq = regex1.search(input_str)
        if kq:
            kq = kq.group(1)
        else:
            kq = ''
        return kq

    def regex_many_value(self, pattern, input_str):
        regex1 = re.compile(pattern)
        kq = regex1.findall(input_str)
        return kq

    def convert(self, text):
        patterns = {
            '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
            '[đ]': 'd',
            '[èéẻẽẹêềếểễệ]': 'e',
            '[ìíỉĩị]': 'i',
            '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
            '[ùúủũụưừứửữự]': 'u',
            '[ỳýỷỹỵ]': 'y'
        }
        """
        Convert from 'Tieng Viet co dau' thanh 'Tieng Viet khong dau'
        text: input string to be converted
        Return: string converted
        """
        output = text
        for regex, replace in patterns.items():
            output = re.sub(regex, replace, output)
            # deal with upper case
            output = re.sub(regex.upper(), replace.upper(), output)
        return output

    def encode_tieng_viet_html(self, string_input):
        dict_char = {
            'à': '&#224;',
            'á': '&#225;',
            'â': '&#226;',
            'ã': '&#227;',

            'À': '&#192;',
            'Á': '&#193;',
            'Â': '&#194;',
            'Ã': '&#195;',

            'è': '&#232;',
            'é': '&#233;',
            'ê': '&#234;',

            'È': '&#200;',
            'É': '&#201;',
            'Ê': '&#202;',

            'ì': '&#236;',
            'í': '&#237;',

            'Ì': '&#204;',
            'Í': '&#205;',

            'ò': '&#242;',
            'ó': '&#243;',
            'ô': '&#244;',

            'Ò': '&#210;',
            'Ó': '&#211;',
            'Ô': '&#212;',

            'ù': '&#249;',
            'ú': '&#250;',

            'Ù': '&#217;',
            'Ú': '&#218;'
        }

        string_output = []
        for char in string_input:
            # print(char)

            if char in dict_char:
                string_output += dict_char[char]
            else:
                string_output += char
        return ''.join(string_output)
