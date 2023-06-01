# Import libraries
from request import count, bnw
import streamlit as st
import numpy as np
import cv2
from PIL import Image


# image = Image.open(r'...\Insights_Bees_logo.png')  # Brand logo image (optional)
def crop_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    ## (2) Morph-op to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    ## (3) Find the max-area contour
    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=cv2.contourArea)[-1]

    ## (4) Crop and save it
    x, y, w, h = cv2.boundingRect(cnt)
    dst = image[y:y + h, x:x + w]
    return dst


def enhance_details(img):
    """
    Enhance the details of the image using the detailEnhance function
    """
    hdr = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
    return hdr


# Create two columns with different width
col1, col2 = st.columns([0.8, 0.2])
with col1:  # To display the header text using css style
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Upload your image here...</p>', unsafe_allow_html=True)

# with col2:  # To display brand logo
#     st.image(image, width=150)

# Add a header and expander in side bar
st.sidebar.markdown('<p class="font">Image Analyser App</p>', unsafe_allow_html=True)
with st.sidebar.expander("About the App"):
    st.write("""
        Use this simple app as a cell counter by uploading your image. \n  \nThis app was created by Raguram and Megahrani. Hope you enjoy!
     """)

# Add file uploader to allow users to upload photos
uploaded_file = st.file_uploader("", type=['jpg', 'png', 'jpeg'])
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        st.markdown('<p style="text-align: center;">Original</p>', unsafe_allow_html=True)
        st.image(image, width=300)

    with col2:
        st.markdown('<p style="text-align: center;">Processed</p>', unsafe_allow_html=True)
        filter = st.sidebar.radio('Convert your photo to:', ['Original', 'Black and White',
                                                             'Enhance Image',
                                                             'Count Cells'])  # Add the filter in the sidebar
        # if filter == 'Gray Image':
        #     converted_img = np.array(image.convert('RGB'))
        #     gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
        #     a = st.image(gray_scale, width=300)
        if filter == 'Black and White':
            # gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
            slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
            # (thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
            blackAndWhiteImage = bnw(image, slider)
            converted_img = np.array(blackAndWhiteImage.convert('RGB'))
            a = st.image(converted_img, width=300)
        elif filter == 'Enhance Image':
            converted_img = np.array(image.convert('RGB'))
            # slider = st.sidebar.slider('Adjust the intensity', 5, 81, 33, step=2)
            converted_img = cv2.cvtColor(converted_img, cv2.COLOR_RGB2BGR)
            # blur_image = cv2.GaussianBlur(converted_img, (slider, slider), 0, 0)
            enhanced_image = enhance_details(converted_img)
            a = st.image(enhanced_image, channels='BGR', width=300)
        elif filter == 'Count Cells':
            # fetching the dimensions
            wid, hgt = image.size

            # displaying the dimensions
            print(str(wid) + "x" + str(hgt))

            image_with_count, num = count(image)
            converted_img = np.array(image_with_count.convert('RGB'))
            image_cropped = converted_img

            # # fetching the dimensions
            # widt, higt = image_cropped.size

            # # displaying the dimensions
            # print(str(widt) + "x" + str(higt))

            # converted_img = np.array(image_with_count.convert('RGB'))
            st.image(image_cropped, channels='BGR', width=300)
            st.text(num)
        else:
            a = st.image(image, width=300)

    # Add a feedback section in the sidebar
    # st.sidebar.title(' ')  # Used to create some space between the filter widget and the comments section
    # st.sidebar.markdown(' ')  # Used to create some space between the filter widget and the comments section
    # st.sidebar.subheader('Please help us improve!')
    # with st.sidebar.form(key='columns_in_form',
    #                      clear_on_submit=True):  # set clear_on_submit=True so that the form will be reset/cleared once it's submitted
    #     rating = st.slider("Please rate the app", min_value=1, max_value=5, value=3,
    #                        help='Drag the slider to rate the app. This is a 1-5 rating scale where 5 is the highest rating')
    #     text = st.text_input(label='Please leave your feedback here')
    #     submitted = st.form_submit_button('Submit')
    #     if submitted:
    #         st.write('Thanks for your feedback!')
    #         st.markdown('Your Rating:')
    #         st.markdown(rating)
    #         st.markdown('Your Feedback:')
