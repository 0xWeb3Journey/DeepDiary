import request from '@/utils/request'

// img api
export function getImg(params) {
  return request({
    url: '/api/img/',
    method: 'get',
    params,
  })
}

export function getImgDetail(id) {
  return request({
    url: '/api/img/' + id + '/',
    method: 'get',
  })
}

export function getMcs(params) {
  return request({
    url: '/api/mcs/' + params.id + '/',
    method: 'get',
    // params,
  })
}
export function getTags(params) {
  return request({
    url: '/api/img/' + params.id + ' / ' + 'set_tags/',
    method: 'get',
  })
}

export function getUploadState(params) {
  return request({
    url: '/api/img/upload_finished/',
    method: 'get',
  })
}

export function doDelete(data) {
  return request({
    url: '/gallery/doDelete',
    method: 'post',
    data,
  })
}

export function upload(data) {
  return request({
    url: '/api/img/',
    method: 'post',
    data,
  })
}

export function getFilterList(params) {
  console.log(params)
  return request({
    url: '/api/img/get_filtered_list/',
    method: 'get',
    params,
  })
}

// get all the gps point from the img database
export function getAddress(params) {
  console.log(params)
  return request({
    url: '/api/address/',
    method: 'get',
    params,
  })
}
