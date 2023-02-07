function downloadFile(file, fileName) {
  var a = document.createElement('a')
  a.href = URL.createObjectURL(file)
  a.download = fileName
  a.hidden = true
  document.body.appendChild(a)
  a.click()
  a.parentNode.removeChild(a)
}

export { downloadFile }
