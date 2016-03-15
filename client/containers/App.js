import React from 'react'
import { Provider, connect } from 'react-redux'
import thunkMiddleware from 'redux-thunk'
import { createStore, applyMiddleware } from 'redux';
import rootReducer from '../reducers';
import { setQuery, setTag, fetchDocuments, fetchTags } from '../actions'
import DocumentTable from '../components/Documents'
import SearchBar from '../components/SearchBar'

class App extends React.Component {
  constructor(props) {
    super(props);
    this.handleEnter = this.handleEnter.bind(this);
  }

  componentDidMount() {
    const { dispatch, currentQuery, currentTag } = this.props;
    dispatch(fetchDocuments(currentQuery, currentTag));
    dispatch(fetchTags());
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.currentQuery !== this.props.currentQuery ||
        nextProps.currentTag !== this.props.currentTag) {
      const { dispatch, currentQuery, currentTag } = nextProps
      dispatch(fetchDocuments(currentQuery, currentTag))
    }
  }

  handleEnter(nextQuery) {
    this.props.dispatch(setQuery(nextQuery));
  }

  render() {
    const { currentQuery, currentTag, documents, tagDefinitions,
            isFetching, lastUpdated } = this.props;
    return (
      <div>
        <div calssName="row">
          <div className="u-full-width">
              <SearchBar value={currentQuery} onEnter={this.handleEnter} />
          </div>
        </div>
        <div className="row">
          {isFetching && documents.length === 0 &&
            <h2>Loading...</h2>
          }
          {!isFetching && documents.length === 0 &&
            <h2>Empty.</h2>
          }
          {documents.length > 0 &&
            <div className="u-full-width"
                 sytle={{ opacity: isFetching? 0.5 : 1 }}>
              <DocumentTable documents={documents}
                             tagDefinitions={tagDefinitions} />
            </div>
          }
        </div>
      </div>
    )
  }
}

App.propTypes = {
  documents: React.PropTypes.array.isRequired,
  isFetching: React.PropTypes.bool.isRequired,
  lastUpdated: React.PropTypes.number,
  dispatch: React.PropTypes.func.isRequired
}

function mapStateToProps(state) {
  const { currentQuery, currentTag, documentsByFilter, tags } = state
  const {
    isFetching: isFetchingTags,
    items: tagDefinitions
  } = tags || {
    isFetching: true,
    items: []
  }
  const {
    isFetching: isFetchingDocuments,
    lastUpdated,
    items: documents
  } = documentsByFilter[currentQuery] || {
    isFetching: true,
    items: []
  }
  const isFetching = (isFetchingDocuments || isFetchingTags);

  return {
    currentQuery,
    currentTag,
    documents,
    tagDefinitions,
    isFetching,
    lastUpdated
  }
}

export default connect(mapStateToProps)(App)
