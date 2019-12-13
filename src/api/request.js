import axios from "axios";



export default async function request(route, options = {}) {
  try {
    const response = await axios({
      method: route.type,
      url: route.path,
      ...options
    });
    return response.data;
  } catch (err) {
    return Promise.reject({
      status: err.response.status,
      message: (!!err.response.data && !!err.response.data.reason) ? err.response.data.reason : err + ""
    });
  }
}

