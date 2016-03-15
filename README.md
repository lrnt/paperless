# Paperless

Paperless is a tool that helps you scan, index and archive your documents.

## Requirements

* [ImageMagick] to convert the document to individual PNGs
* [Teseract] to convert the document into readable and searchable text
* [Flask] to serve a REST API
* [NPM] to install the various JS libraries used by the client
    * [Webpack] to bundle JS, CSS and images.
    * [React]
    * [Redux]

[ImageMagick]: http://imagemagick.org
[Teseract]: http://github.com/tesseract-ocr
[Flask]: http://flask.pocoo.org/
[NPM]: http://npmjs.com/
[Webpack]: http://webpack.github.io/
[React]: http://facebook.github.io/react/
[Redux]: http://redux.js.org/

## Storage directory structure
```
.
+ 2016-02-12_12-12-12_96a5e1442c4cf2ec8856cec496732a93edfd4ed0
|   +-- metadata.json
|   +-- original.pdf
|   \-- pages
|       +-- 0001.png
|       +-- 0001.txt
|       +-- 0002.png
|       \-- 0002.txt
|
\-- 2015-01-12_12-12-14_0f46d81cbca4929ec0af34b3e57d2a036eb1a315
    +-- metadata.json
    +-- original.pdf
    \-- pages
        +-- 0001.png
        +-- 0001.txt
        +-- 0002.png
        \-- 0002.txt
```

## metadata.json
```
{
    "tags": [
        "invoice",
        "home-utility"
    ],
    "datetime_scan": "2015-12-24T11:52:58.214225",
    "datetime_document": "",
    "original_name": "scan-11023.pdf",
    "sha1": "0f46d81cbca4929ec0af34b3e57d2a036eb1a315",
    "title": ""
}
```
