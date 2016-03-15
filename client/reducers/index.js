import { combineReducers } from 'redux';
import { SET_QUERY, SET_TAG, REQUEST_DOCUMENTS, RECIEVE_DOCUMENTS, REQUEST_TAGS, RECIEVE_TAGS } from '../actions';

function currentQuery(state = '', action) {
  switch (action.type) {
    case SET_QUERY:
      return action.query;
    default:
      return state;
  }
}

function currentTag(state = '', action) {
  switch (action.type) {
    case SET_TAG:
      return action.tag;
    default:
      return state;
  }
}

function documents(state = {
  isFetching: false,
  items: []
}, action) {
  switch (action.type) {
    case REQUEST_DOCUMENTS:
      return Object.assign({}, state, {
        isFetching: true
      });
    case RECIEVE_DOCUMENTS:
      return Object.assign({}, state, {
        isFetching: false,
        items: action.documents,
        lastUpdated: action.recievedAt
      });
    default:
      return state;
  }
}

function documentsByFilter(state = {}, action) {
  switch (action.type) {
    case RECIEVE_DOCUMENTS:
    case REQUEST_DOCUMENTS:
      return Object.assign({}, state, {
          [action.query]: documents(state[action.query], action)
      });
    default:
      return state;
  }
}

function tags(state = {
  isFetching: false,
  items: []
}, action) {
  switch (action.type) {
    case REQUEST_TAGS:
      return Object.assign({}, state, {
        isFetching: true
      });
    case RECIEVE_TAGS:
      return Object.assign({}, state, {
        isFetching: false,
        items: action.tags
      });
    default:
      return state;
  }
}

const rootReducer = combineReducers({
  tags,
  documentsByFilter,
  currentQuery,
});

export default rootReducer
