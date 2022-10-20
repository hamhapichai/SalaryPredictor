import streamlit as st
import pandas as pd
from autogluon.tabular import TabularPredictor
import pathlib
import platform
plt =  platform.system()
if plt == 'Windows': pathlib.PosixPath = pathlib.WindowsPath

import dclean as dclean

def setup_page():
    st.set_page_config(
        page_title='LittleHR, IT Salary Estimator',
        page_icon=':computer:',
        layout='centered',
    )
    css = open('app/style.css','r')
    st.markdown(f'<style> {css.read()} </style>',unsafe_allow_html=True)

    font = open('app/font.txt','r')
    st.markdown(f'{font.read()}',unsafe_allow_html=True)

def input_thingy():
    col1, col2 = st.columns(2)
        
    # Options ls
    if True:
        province_option = (
        'กรุงเทพมหานคร (Bangkok)','นนทบุรี (Nonthaburi)','ปทุมธานี (Pathum Thani)','สมุทรปราการ (Samut Prakan)','กาญจนบุรี (Kanchanaburi)','จันทบุรี (Chanthaburi)','ฉะเชิงเทรา (Chachoengsao)','ชลบุรี (Chonburi)','ชัยนาท (Chai Nat)','ตราด (Trad)','นครนายก (Nakhon Nayok)','นครปฐม (Nakhon Pathom)','ประจวบคีรีขันธ์ (Prachuap Kiri Kan)','ปราจีนบุรี (Prachin Buri)','พระนครศรีอยุธยา (Phra Nahhon Si Ayutthaya)','เพชรบุรี (Phetchaburi)','ระยอง (Rayong)','ราชบุรี (Ratchaburi)','ลพบุรี (Lopburi)','สมุุทรสงคราม (Samut  Songkhram)','สมุทรสาคร (Samut Sakhon)','สระแก้ว (Sa Kaeo)','สระบุรี (Saraburi)','สิงห์บุรี (Singburi)','สุพรรณบุรี (Suphanburi)','อ่างทอง (Ang Thong)','กำแพงเพชร (Kamhaeng Phet)','เชียงราย (Chiang Rai)','เชียงใหม่ (Chiang Mai)','ตาก (Tak)','นครสวรรค์ (Nakhon Sawan)','น่าน (Nan)','พะเยา (Payao)','พิจิตร (Phichit)','พิษณุโลก (Phitsanulok)','เพชรบุูรณ์ (Phetchabun)','แพร่ (Prae)','แม่ฮ่องสอน (Mae Hong Son)','ลำปาง (Lumpang)','ลำพูน (Lumpoon)','สุโขทัย (Sukhothai)','อุตรดิตถ์ (Uttaradit)','อุทัยธานี (Uthai Thani)','กาฬสินธุ์ (Kalasin)','ขอนแก่น (Khon Kaen)','ชัยภูมิ (Chaiyaphum)','นครพนม (Nakhon Phanom)','นครราชสีมา (Nakhon Ratchasima)','บุรีรัมย์ (Buriram)','มหาสารคาม (Maha Sarakham)','มุกดาหาร (Mukdahan)','ยโสธร (Yasothon)','ร้อยเอ็ด (Roi Et)','เลย (Loei)','ศรีสะเกษ (Sri Saket)','สกลนคร (Sakon Nakhon)','สุรินทร์ (Surin)','หนองคาย (Nong Khai)','หนองบัวลำภู (Nong Bua Lamphu)','อุดรธานี (Udon Thani)','อุบลราชธานี (Ubon Ratchathani)','อำนาจเจริญ (Amnat Charoen)','บึงกาฬ (Bueng Kan)','กระบี่ (Krabi)','ชุมพร (Chumphon)','ตรัง (Trang)','นครศรีธรรมราช (Nakhon Sri Thammarat)','นราธิวาส (Narathiwat)','ปัตตานี (Pattani)','พังงา (Phang Nga)','พัทลุง (Phatthalung)','ภูเก็ต (Phuket)','ยะลา (Yala)','ระนอง (Ranong)','สงขลา (Songkla)','สตูล (Satun)','สุราฎร์ธานี (Surat Thani)'
        )
        edu_option = (
        'ต่ำกว่ามัธยมศึกษา (Lower than Secondary School)',
        'มัธยมศึกษาตอนต้น (Middle School)',
        'มัธยมศึกษาตอนปลาย (High School)',
        'ปวช. (Vocational Certificate)',
        'ปวส. (High Vocational Certificate)',
        'ปริญญาตรี (Bachelor\'s Degree)',
        'ปริญญาโท (Master\'s Degree)',
        'ปริญญาเอก (Doctoral\'s Degree or PhD)',
        )
        dev_options = (
        'Data scientist or machine learning specialist',
        'Scientist',
        'Academic researcher',
        'Data engineer',
        'Front-end developer',
        'QA or test developer',
        'Designer',
        'Full-stack developer',
        'Data or business analyst',
        'Back-end developer',
        'Database administrator',
        'Product manager',
        'Marketing or sales professional',
        'Engineering manager',
        'System administrator',
        'Embedded applications or devices developer',
        'Mobile developer',
        'Game or graphics developer',
        'Desktop or enterprise applications developer',
        'Educator',
        'DevOps specialist',
        'Site reliability engineer',
        'Senior Executive (C-Suite/VP/etc.)',
        'Consultant',
        'Cloud Engineer',
        'UX/UI Developer',
        'Web Developer',
        'IT Security',
        'Penetration tester',
        'Manager',
        'IT Support',
        'Network Engineer',
        'Security Engineer',
        'Business Intelligence',
        'UI/UX Designer',
        'Human Resource',
        'Robotic Software Engineer',
        'CTO',
        'Director',
        'CEO',
        'Software engineer',
        'System Analyst',
        )
        orgsize_options = (
        'มีคนเดียว ทำทุกตำแหน่ง (Freelancer/Just me)',
        '2 คนขึ้นไป แต่ไม่เกิน 20 คน (2 to 19 employees)',
        '20 คนขึ้นไป แต่ไม่เกิน 100 คน (20 to 99 employees)',
        '100 คนขึ้นไป แต่ไม่เกิน 1,000 คน (100 to 999 employees)',
        '1,000 คนขึ้นไป แต่ไม่เกิน 10,000 คน (1,000 to 9,999 employees)',
        '10,000 คนขึ้นไป (10,000 or more employees)',
        )
    # EdLevel
    edlv = col1.selectbox(
    '🏫วุฒิการศึกษาสุดท้าย',
    index = 5,
    options=edu_option,)
    # WorkPlace
    workplace = col2.selectbox(
        '🏢จังหวัดที่ทำงาน/จังหวัดที่องค์กรอยู่',
        options=province_option)
    # YearsCodePro
    code_pro = col1.number_input(
        '🧰มีประสบการณ์การทำงานกี่ปี?',
        min_value=0.0,
        max_value=50.0,
            step=0.5)
    # YearsCode
    code = col1.number_input(
        '🖥️มีประสบการณ์การเขียนโปรแกรมหรือประสบการณ์ทำงานทั้งหมดเกี่ยวกับอาชีพที่ทำกี่ปี? (รวมช่วงที่ทำอาชีพด้วย)',
        min_value=0.0,
        max_value=50.0,
        step=0.5)
    # if code < code_pro:
    #     code += code_pro
    # DevType
    devtype_arr = col2.multiselect(
        '🖱️ตำแหน่งงาน',
        options=dev_options)
    devtype = ', '.join(devtype_arr)
    # OrgSize
    orgsize = col2.selectbox(
        '🏢ขนาดองค์กร',
        options=orgsize_options)
    # Employment
    employ = col2.radio(
        '⏰ประเภทงานจ้างแบบ',
        options=['Full-time','Part-time','Freelance'],
        horizontal=True)

    data_input = {
            'WorkPlace': dclean.wplace(workplace),
            'EdLevel': dclean.edu(edlv),
            'YearsCodePro': code_pro,
            'YearsCode': code,
            'Employment': dclean.employ(employ),
            'DevType': devtype,
            'OrgSize': dclean.orgsize(orgsize),
        }
    data_input = pd.DataFrame(data=data_input, index=[0])
    return data_input

def salary_display(salary):
    offset = salary * 0.03
    low = '{}'.format(round(salary - offset))
    high = '{}'.format(round(salary + offset))

    salary = [low, high]

    for s in range(2):
        front = salary[s][:len(salary[s])%3]
        salary[s] = salary[s][len(salary[s])%3:]
        back = ''
        for i in range(len(salary[s])):
            if i % 3 == 0:
                back += ','
            back += salary[s][i]
        
        if front != '':
            salary[s] = front + back
        else:
            salary[s] = back[1:]
    
    return f'🏷️{salary[0]} - {salary[1]} บาท/เดือน'

def sidebar_thingy():
    with st.sidebar:
        st.markdown('<bighead>โปรเจ็คเทอมวิชาปัญญาประดิษฐ์</bighead>', unsafe_allow_html=True)
        st.markdown('<bighead>📜 About this project</bighead>', unsafe_allow_html=True)
        st.markdown('<text style=\'font-size:14px;\'>โปรเจคนี้เป็นส่วนหนึ่งของวิชาปัญญาประดิษฐ์ พัฒนาขึ้นเพื่อประเมินเงินเดือนของอาชีพสาย IT ตามข้อมูลตำแหน่งงานและประสบการณ์ของพนักงาน โดยใช้ Machine Learning Regression Model ที่เทรนด้วยข้อมูลจากการทำแบบสอบถามผู้ประกอบอาชีพสาย IT ผ่าน Social Media ในปีพ.ศ.2565</text>',unsafe_allow_html=True)

def output_thingy(data_input, m):
    
    # st.write(data_input)

    predictor = TabularPredictor.load('app/ag-models')
    result = predictor.predict(data_input)

    st.header('เงินเดือนของคุณคือ')

    st.title(salary_display(result.values[0] * m * 1e4))

if __name__ == '__main__':
    setup_page()

    st.markdown(
        """
        <text style="font-size: 60px;font-family:'Sarabun', sans-serif;font-weight: bold;">🔍LittleHR</text>
        <text style="font-size: 30px;font-family: 'Sarabun', sans-serif;font-weight: bold;">: Thai IT Job's Salary Estimator</text><br>
        <text style="font-size: 30px;font-family: 'Sarabun', sans-serif;font-weight: bold;padding:0px 0px 0px 60px">โมเดลประเมินเงินเดือนอาชีพสาย IT ในประเทศไทย</text>
        """
        ,unsafe_allow_html=True)

    ## sidebar_thingy()
   
    st.header(' ')
    with st.form('my_form'):

        data_input = input_thingy()
        
        if st.form_submit_button('🔍 ประเมิน'):
            m = 1
            if data_input.at[0,'Employment'] == 0:
                m = 0.75
            
            if data_input.at[0,'DevType'] != '':
                with st.spinner('กำลังคิดอยู่ อย่าเร่งกันสิ...'):
                    output_thingy(data_input, m)
            else:
                st.error('โปรดตอบคำถามให้ครบถ้วนก่อนเริ่มประเมิน')

    