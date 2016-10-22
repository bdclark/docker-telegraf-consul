FROM telegraf:alpine

ENV TELEGRAF_CONF_KEY=telegraf

ENV DUMB_INIT_VERSION 1.1.3
RUN set -ex \
  && apk add --no-cache curl python \
  && curl -fsLo /usr/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v${DUMB_INIT_VERSION}/dumb-init_${DUMB_INIT_VERSION}_amd64 \
  && chmod +x /usr/bin/dumb-init \
  && apk del curl

# Not used at this time - custom patched consul-template for toTOML support
# See https://github.com/hashicorp/consul-template/pull/749
#
# ENV CONSUL_TEMPLATE_VERSION 0.16.0
# RUN set -ex \
#   && apk add --no-cache curl zip \
#   && curl -fsLo temp.zip https://releases.hashicorp.com/consul-template/${CONSUL_TEMPLATE_VERSION}/consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.zip \
#   && unzip temp.zip -d /usr/bin \
#   && rm temp.zip \
#   && apk del curl zip

COPY etc /etc/
COPY bin /usr/bin/

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/usr/bin/consul-template", "-config=/etc/consul-template.d"]
