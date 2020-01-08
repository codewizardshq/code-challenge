import axios from "axios";
import routes from "./routes";

export default async function request(route, options = {}, tryRefresh = true) {
  try {
    // attempt initial request and return great response
    const response = await axios({
      method: route.type,
      url: route.path,
      ...options
    });
    return response.data;
  } catch (err) {
    if (err.response.status == 401 && tryRefresh) {
      // our tokens have possibly expired, send refresh
      // TODO: THIS IS UNFINISHED
      await axios({
        method: "POST",
        url: routes.userapi_refresh.path
      });

      // try and return original request marked with no refresh
      return request(route, options, false);
    }

    // return original error
    return Promise.reject({
      status: err.response.status,
      message:
        !!err.response.data && !!err.response.data.reason
          ? err.response.data.reason
          : err + ""
    });
  }
}
