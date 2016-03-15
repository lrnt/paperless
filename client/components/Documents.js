import React from 'react'

export default class DocumentTable extends React.Component {
  render() {
    let {documents, tagDefinitions} = this.props;
    let rows = documents.map((document, id) => {
      return (
        <DocumentItem document={document}
                      tagDefinitions={tagDefinitions}
                      key={id} />
      )
    });
    return (
      <div className="row">
        <div className="ul-full-width">
          <table className="u-full-width">
            <thead>
              <tr>
                <th></th>
                <th>Name</th>
                <th>Date</th>
                <th>Tags</th>
              </tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
      </div>
    );
  }
}


class DocumentItem extends React.Component {
  render() {
    let tagDefinitions = this.props.tagDefinitions;
    let {original_name, datetime_scan, sha1} = this.props.document;
    let url = `/documents/{sha1}`
    let tags = this.props.document.tags.map((tag, id) => {
      let color = tagDefinitions[tag];
      return (
        <DocumentTag tag={tag} color={tagDefinitions[tag]} key={id} />
      )
    });
    return (
      <tr>
        <td>
          <a href={`/documents/${sha1}`}>
            <img src={require('../images/download.png')} />
          </a>
        </td>
        <td>{original_name}</td>
        <td><TimeAgo date={datetime_scan} /></td>
        <td>{tags}</td>
      </tr>
    );
  }
}


class DocumentTag extends React.Component {
  render() {
    let style = {backgroundColor: this.props.color};
    return (
      <span className="tag" style={style}>
        {this.props.tag}
      </span>
    );
  }
}

class TimeAgo extends React.Component {
  render() {
    let date = this.props.date;
    let then = (new Date(date)).valueOf();
    let now = Date.now();
    let seconds = Math.round(Math.abs(now - then) / 1000)
    let value, unit;

    if(seconds < 60){
      value = Math.round(seconds);
      unit = 'second';
    } else if(seconds < 60*60) {
      value = Math.round(seconds/60);
      unit = 'minute';
    } else if(seconds < 60*60*24) {
      value = Math.round(seconds/(60*60));
      unit = 'hour';
    } else if(seconds < 60*60*24*7) {
      value = Math.round(seconds/(60*60*24));
      unit = 'day';
    } else if(seconds < 60*60*24*30) {
      value = Math.round(seconds/(60*60*24*7));
      unit = 'week';
    } else if(seconds < 60*60*24*365) {
      value = Math.round(seconds/(60*60*24*30));
      unit = 'month';
    } else {
      value = Math.round(seconds/(60*60*24*365));
      unit = 'year';
    }

    let suffix = value > 1 ? 's' : '';
    let ago = value + ' ' + unit + suffix;
    return (
      <abbr title={date}>
        <time dateTime={date}>{ago}</time>
      </abbr>
    );
  }
}
