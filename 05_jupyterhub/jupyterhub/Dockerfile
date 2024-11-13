FROM quay.io/jupyterhub/jupyterhub


RUN apt-get update -y && apt-get install -y python3-pip \
    && apt-get install -y sudo \
    && apt-get install -y nano \
    && pip3 install --upgrade pip \
    && apt-get install -y software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update -y \ 
    &&  apt-get install -y git-all \
    && apt install -y python3.10-venv \
    && apt-get install -y r-base \
    && apt-get install -y libcurl4-openssl-dev \
    && apt-get install -y libxml2-dev

# RUN python3 -m pip install notebook
RUN python3 -m pip install oauthenticator
RUN pip3 install --upgrade jupyterlab jupyterlab-git

RUN R -e "install.packages('IRkernel', repos='http://cran.r-project.org')" \
    && R -e "IRkernel::installspec(user = FALSE)"

COPY ./notebooks /srv/notebooks

RUN jupyterhub --generate-config
