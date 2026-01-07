FROM openquantumsafe/oqs-ossl3

RUN apk update && apk add --no-cache \
    iproute2 \
    tcpdump \
    bash

CMD ["tail", "-f", "/dev/null"]