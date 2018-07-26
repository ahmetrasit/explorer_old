

var fileSelect = document.getElementById('file-select');
var selected_files
var file_types
var data_type = ''




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
    data_type = [...file_types][0]
    var existing_category = data_categories.indexOf(data_type)
    if (existing_category > -1) {
      document.getElementById('data_categories_select').selectedIndex = existing_category+1
    }else {
      alert('Be sure that you choose the right data category for uploaded file(s)')
    }
    if (selected_files.length == 1){
      d3.select('#single_input').style('display', 'block')
      $('#file_label').html('1 file with the following data category: ' + data_type)
    }else {
      d3.select('#multiple_inputs').style('display', 'block')
      $('#file_label').html(selected_files.length + ' files with the following data category: ' + data_type)
    }
    prepareFields(selected_files.length)
    d3.select('.custom-file').style('box-shadow', 'none')
  }else if (file_types.size > 1) {
    alert('Please be sure that all files are of the same type.')
    d3.select('.custom-file').style('box-shadow', '1px 1px 5px 5px red')
    data_type = ''
  }else {
    data_type = ''
  }

}

function prepareFields(no_of_files) {
  console.log(data_type);
  var sample_input_fields = ['sample name', 'type', 'description']
  addSampleInputPerFile(sample_input_fields)
  d3.selectAll('.show_only_samples').selectAll('div').remove()
  addSampleInputPerSample(sample_input_fields, false)
  addSampleInputButton(sample_input_fields)
}


function addSampleInputPerFile(sample_input_fields) {
  d3.selectAll('.show_also_filename').selectAll('div').remove()
  var curr_input = d3.selectAll('.show_also_filename').selectAll('div').data(selected_files).enter()
                      .append('div').attr('class', 'input-group mb-2').attr('id', function(d,i){return d})
  curr_input.append('div').attr('class', 'input-group-prepend col-md-3  mx-0 px-0').attr('data-toggle', 'tooltip').attr('title', function(d){return d})
    .append('span').attr('class', 'input-group-text form-control mx-0').html(function(d,i){return d})
  curr_input.selectAll('input').data(sample_input_fields).enter()
    .append('input').attr('type', 'text').attr('class', 'form-control').attr('data-bv-notempty', true)
    .attr('placeholder', function(d,i){return d}).attr('name', function(d,i){console.log(this.parentNode.id); return this.parentNode.id + "_" + d})
}


function addSampleInputPerSample(sample_input_fields, active) {
  var curr_input
  if (active) {
    curr_input = d3.selectAll('.active').selectAll('.show_only_samples').append('div').attr('class', 'input-group mb-2')
  }else {
    curr_input = d3.selectAll('.show_only_samples').append('div').attr('class', 'input-group mb-2')
  }
  curr_input.selectAll('input').data(sample_input_fields).enter()
    .append('input').attr('type', 'text').attr('class', 'form-control')
    .attr('placeholder', function(d,i){return d}).attr('name', function(d,i){return d.replace(/\W/g, '_')})

  curr_input.append('div').attr('class', 'input-group-append')
    .append('span').on('click', removeThis).attr('class', 'input-group-text btn btn-danger').html('<i class="fas fa-trash-alt"></i>')
}


function addSampleInputButton(sample_input_fields) {
  d3.selectAll('.multi_samples').selectAll('button').remove()
  var curr_input = d3.selectAll('.multi_samples')
    .append('button').on('click', function(){addSampleInputPerSample(sample_input_fields, true)})
      .attr('type', 'button')
      .attr('class', 'col-md-12 btn btn-success btn-block')
      .html('<i class="fas fa-plus-circle"></i> Add new sample info')
}


function removeThis() {
  if ($(this).parent().parent().parent()[0].childElementCount > 1) {
      $(this).parent().parent().remove();
  }
}


function activeInputsNotEmpty() {
  valid = true
  for (variable of $('.active').find('div:visible').find('input')) {
    if (variable.value.trim().length < 1 ) {
      valid = false
      console.log(variable);
      variable.style['box-shadow'] = 'inset 0px 0px 3px 3px red'
    }else {
      variable.style['box-shadow'] = 'none'
    }
  }
  return valid
}


function uploadFiles(){

  var files = fileSelect.files;
  var formData = new FormData();
  for (var i = 0; i < files.length; i++) {
    var file = files[i];
    formData.append('filesToUpload', file, file.name);
    selected_files.push(file.name)
  }

   for (variable of $('.active').find('div:visible').find('input')) {
     console.log(variable.name);
     console.log(variable.value);
     formData.append(variable.name, variable.value.trim())
   }

  var xhr = new XMLHttpRequest()
  xhr.open('POST', '/upload/', true);
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

  if (fileSelect.files.length > 0) {
    if (activeInputsNotEmpty()) {
      xhr.send(formData);
      $('#file_label').html('Choose file')
      d3.selectAll('.noof_inputs').style('display', 'none')
      $('#fileUploadModal').modal('hide')
    }
  }else {
    d3.select('.custom-file').style('box-shadow', '0px 0px 3px 3px red')
  }

}


function uploadFileTypeChange(){
  if (data_type.length > 0) {
    data_type = this.options[this.selectedIndex].value
    prepareFields()
  }

}
