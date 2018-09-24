import fetch from 'dva/fetch';

const apServUrl ="http://192.168.0.208:5000"
//const apServUrl ="http://localhost:5000"

function parseJSON(response) {
  return response.json();
}

function checkStatus(response) {
  //console.log( response.json() )

  if (response.status >= 200 && response.status < 300) {
    return response;
  }

  const error = new Error(response.statusText);
  error.response = response;
  throw error;
}

/**
 * Requests a URL, returning a promise.
 *
 * @param  {string} url       The URL we want to request
 * @param  {object} [options] The options we want to pass to "fetch"
 * @return {object}           An object containing either "data" or "err"
 */


export default function request(path, options) {
  let url = apServUrl + path
  return fetch(url, options)
    .then(checkStatus)
    .then(parseJSON)
    .then(data => ({ data }))
    .catch(err => ({ err }));
}


