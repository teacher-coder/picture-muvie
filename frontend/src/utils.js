function downloadFile(data, fileName) {
  const url = URL.createObjectURL(new Blob([data]))
  const link = document.createElement('a')
  document.body.appendChild(link)
  link.href = url
  link.hidden = true
  link.setAttribute('download', fileName)
  link.click()
  document.body.removeChild(link)
  link.remove()
}

export { downloadFile }
