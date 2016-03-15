'use strict';

import fetch from 'isomorphic-fetch';

const API_ROOT = `${location.protocol}${location.host}`

export const SET_QUERY = 'SET_QUERY'
export const SET_TAG = 'SET_TAG'
export const REQUEST_TAGS = 'REQUEST_TAGS';
export const RECIEVE_TAGS = 'RECIEVE_TAGS';
export const REQUEST_DOCUMENTS = 'REQUEST_DOCUMENTS';
export const RECIEVE_DOCUMENTS = 'RECIEVE_DOCUMENTS';
export const EDIT_DOCUMENT = 'EDIT_DOCUMENT';
export const SAVE_DOCUMENT = 'SAVE_DOCUMENT';

export function setQuery(query) {
  return {
    type: SET_QUERY,
    query
  };
}

export function setTag(tag) {
  return {
    type: SET_TAG,
    tag
  };
}

export function requestTags() {
  return {
    type: REQUEST_TAGS
  };
}

export function recieveTags(json) {
  return {
    type: RECIEVE_TAGS,
    tags: json
  };
}

export function editDocument(key) {
  return {
    type: EDIT_DOCUMENT,
    key
  };
}

export function saveDocument(key, json) {
  return {
    type: SAVE_DOCUMENT,
    document: json,
    key
  };
}

export function fetchTags() {
  return dispatch => {
    dispatch(requestTags())
    return fetch(`${API_ROOT}/tags/`)
      .then(response => response.json())
      .then(json => dispatch(recieveTags(json)));
  }
}

export function requestDocuments(query, tag) {
  return {
    type: REQUEST_DOCUMENTS,
    query,
    tag
  };
}

export function recieveDocuments(query, tag, json) {
  return {
    type: RECIEVE_DOCUMENTS,
    query,
    tag,
    documents: json,
    recievedAt: Date.now()
  };
}

export function fetchDocuments(query, tag) {
  return dispatch => {
    dispatch(requestDocuments(query, tag))
    return fetch(`${API_ROOT}/documents/?q=${query}`)
      .then(response => response.json())
      .then(json => dispatch(recieveDocuments(query, tag, json)));
  }
}
