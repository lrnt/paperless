import React from 'react'
import debounce from 'debounce'

export default class SearchBar extends React.Component {
  constructor() {
    super();
    this.onChange = debounce(this.onChange, 200);
  }

  onChange(value) {
    this.props.onEnter(value);
  }

  render() {
    return (
      <input onChange={e => this.onChange(e.target.value)} type="text" />
    )
  }
}

SearchBar.propTypes = {
  value: React.PropTypes.string.isRequired,
  onEnter: React.PropTypes.func.isRequired
}
