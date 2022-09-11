import request from '@/utils/request'

export function getAlbum(params) {
  return request({
    url: '/api/img/',
    method: 'get',
    params,
  })
}

export function getGallery(params) {
  return request({
    url: '/api/img/',
    method: 'get',
    params,
  })
}

export function getImg(params) {
  return request({
    url: '/api/img/' + params.id + '/',
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

export function checkImgMcs(params) {
  return request({
    url: '/api/img/check_mcs/',
    method: 'get',
  })
}

export function getFaceAlbum(params) {
  return request({
    url: '/api/faces/',
    method: 'get',
    params,
  })
}
export function getFaceAlbumDetail(params) {
  return request({
    url: '/api/faces/' + params.id + '/',
    method: 'get',
    params,
  })
}

export function changeFaceAlbumName(data) {
  return request({
    url: '/api/faces/' + data.id + '/',
    method: 'put',
    data,
  })
}

export function clear_face_album(params) {
  return request({
    url: '/api/faces/clear_face_album/',
    method: 'get',
  })
}

export function getFace(params) {
  return request({
    url: '/api/face/' + params.id + '/',
    method: 'get',
    // params,
  })
}

export function changeFaceName(data) {
  return request({
    url: '/api/face/' + data.id + '/',
    method: 'put',
    data,
  })
}

// export function getFaceGallery(params, id) {
//   console.log(params)
//   return request({
//     url: '/api/faces/' + id + '/',
//     method: 'get',
//     params,
//   })
// }

export function getFaceGallery(params) {
  console.log(params)
  return request({
    url: '/api/face/',
    method: 'get',
    params,
  })
}

export function doEdit(data) {
  return request({
    url: '/gallery/doEdit',
    method: 'post',
    data,
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
