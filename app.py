import time
import streamlit as st
import numpy as np
from PIL import Image
import urllib.request
from utils import *

labels = gen_labels()

html_temp = '''
    <div style =  padding-bottom: 20px; padding-top: 20px; padding-left: 5px; padding-right: 5px">
    <center><h1>Phân loại rác thải</h1></center>
    
    </div>
    '''

st.markdown(html_temp, unsafe_allow_html=True)
html_temp = '''
    <div>
    <h2></h2>
    <center><h3>Vui lòng cho tôi xem ảnh bạn muốn phân loại</h3></center>
    </div>
    '''
st.set_option('deprecation.showfileUploaderEncoding', False)
st.markdown(html_temp, unsafe_allow_html=True)
opt = st.selectbox("Bạn muốn tải ảnh lên để phân loại thì làm như thế nào?\n", ('Danh mục chọn', 'Tải lên hình ảnh qua liên kết', 'Tải ảnh từ file trong máy của bạn'))
if opt == 'Tải ảnh từ file trong máy của bạn':
    file = st.file_uploader('Chọn', type = ['jpg', 'png', 'jpeg'])
    st.set_option('deprecation.showfileUploaderEncoding', False)
    if file is not None:
        image = Image.open(file)

elif opt == 'Tải lên hình ảnh qua liên kết':

  try:
    img = st.text_input('Nhập địa chỉ hình ảnh')
    image = Image.open(urllib.request.urlopen(img))
    
  except:
    if st.button('Phân loại'):
      show = st.error("Vui lòng nhập địa chỉ hình ảnh hợp lệ!")
      time.sleep(4)
      show.empty()

try:
  if image is not None:
    st.image(image, width = 300, caption = 'Tải ảnh')
    if st.button('Phân loại nào'):
        img = preprocess(image)

        model = model_arc()
        model.load_weights("D:\Machine Learning\BTL\Web App\model.h5")

        prediction = model.predict(img[np.newaxis, ...])
        st.info('Hình ảnh bạn muốn phân loại thuộc " {} waste " '.format(labels[np.argmax(prediction[0], axis=-1)]))
except Exception as e:
  st.info(e)
  pass