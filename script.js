function getPage (page, callback) {
url = "https://s3.amazonaws.com/dcstat/metadata.json"
$.getJSON(url, function (d){
  // find the first end page that's greater than or equal to the page
  console.log(d)
  // diff = page + 1 - start
  callback(measure_url#page=diff)
})
}