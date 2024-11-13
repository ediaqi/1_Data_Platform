from constants import *


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        image('https://ediaqi.eu/themes/custom/ediaqi01/images/favicon.ico',
              width=px(25), height=px(25)),
        "The EDIAQI project is a European funded research and innovation action under the Horizon Europe framework programme. ",
        br(), "Visit: ",
        link("https://ediaqi.eu/", "https://ediaqi.eu/"),
        br(),
        link("https://www.know-center.at/", 
             image('https://www.know-center.at/wp-content/themes/kc-theme/assets/images/know-center-logo.svg', width=px(50), height=px(25))),
    ]
    layout(*myargs)


def display_header():
    st.set_page_config(
            page_title="EDIAQI Dashboard",
            page_icon="./images/favicon.ico",
            layout="wide")
    c1, _, _, _, _, _, _, c8 = st.columns(8)
    c1.image('./images/ediaqi-logo-light.svg')
    c8.image('./images/atl.site.png')
    st.title('Data Monitoring')

