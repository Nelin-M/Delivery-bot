FROM python:3.10
# set work directory
WORKDIR /usr/src/app/
# copy project
COPY . .
# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN echo "export PATH=$PATH:~/.local/share/pypoetry/venv/bin" >> ~/.bashrc
ENV PATH ~/.local/share/pypoetry/venv/bin:${PATH}
# init virtual env
RUN bash -c "poetry env use python3.10"
# install dependencies
RUN bash -c "poetry install --only main"
# run app
CMD bash -c "poetry run python -m src.main"