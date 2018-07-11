

var fileSelect = document.getElementById('file-select');
var selected_files
var file_types


fileSelect.onchange = function(event){
  selected_files = []
  file_types = new Set()
  var files = fileSelect.files;
  for (var i = 0; i < files.length; i++) {
    var file = files[i];
    selected_files.push(file.name)
    file_types.add(file.name.replace(/^[^.]+\./, ''))
  }

  d3.selectAll('.noof_inputs').style('display', 'none')
  $('#file_label').html('Choose file')
  if (file_types.size == 1) {
    if (selected_files.length == 1){
      d3.select('#single_input').style('display', 'block')
      $('#file_label').html('1 file selected')
    }else {
      d3.select('#multiple_inputs').style('display', 'block')
      $('#file_label').html(selected_files.length + ' files selected')
    }
  }else if (file_types.size > 1) {
    alert('Please be sure that all files are in the same type.')
  }else {
    //do nothing
  }

}

function uploadFiles(){

  var files = fileSelect.files;
  var formData = new FormData();
  for (var i = 0; i < files.length; i++) {
    var file = files[i];
    formData.append('filesToUpload', file, file.name);
    selected_files.push(file.name)
  }

  var xhr = new XMLHttpRequest()
  xhr.open('POST', '/uploadFASTQ/', true);
  xhr.upload.addEventListener('progress', onProgress, false);

  function onProgress(e) {
    if (e.lengthComputable) {
      var perc = parseInt(100 * e.loaded / e.total)
      $('#progressbar').attr('style', 'width:'+perc+'%')
    }
  }

  xhr.onload = function () {
    if (xhr.status === 200) {
      alert('File(s) uploaded.')
    } else {
      alert('Sorry, there is something wrong. Maybe the server is down, or you lost connection.');
    }
  };

  xhr.onloadstart = function (e) {
      $('#progress-bar-container').attr('style', 'visibility:visible')
  }
  xhr.onloadend = function (e) {
      $('#progress-bar-container').attr('style', 'visibility:hidden')
  }

  xhr.send(formData);
}


function deleteRow(e){
  e.parentNode.parentNode.parentNode.parentNode.remove()
}
