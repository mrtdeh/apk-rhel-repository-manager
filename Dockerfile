FROM centos as BaseReprepo
LABEL version=1.3
ONBUILD RUN date
RUN yum update
RUN yum install python  pip createrepo -y && yum clean all

FROM BaseReprepo as PipInstall
COPY ./requirements.txt requirements.txt
RUN pip install  --no-cache-dir  -r requirements.txt

FROM PipInstall as CopyFiles
RUN mkdir -p /usr/share/apk_reprepro
RUN mkdir -p /etc/apk_reprepro
RUN mkdir -p /opt/reprepro
COPY . /usr/share/apk_reprepro  
COPY ./config/config.yml /etc/apk_reprepro/
RUN rm -rf /usr/share/apk_reprepro/reprepro.tar.gz


FROM CopyFiles as Build

EXPOSE 8080 80 443
WORKDIR /usr/share/apk_reprepro/

CMD ["/usr/share/apk_reprepro/run.sh"]

# CMD ["gunicorn","-c", "gunicorn.py", "wsgi:app"]
# ENTRYPOINT /usr/share/apk_reprepro/run.sh



