FROM mcr.microsoft.com/playwright

RUN cd $(mktemp -d) && \
    npx playwright install --with-deps && \
    npm i -D @playwright/test

CMD cd /proj && \
    npx playwright test
