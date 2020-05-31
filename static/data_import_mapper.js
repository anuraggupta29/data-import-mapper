var i;
var htmlcontent;
for (i = 0; i < 50; i++) {
  htmlcontent = `<div class="entry"><div class="indexNo"></div><div class="name"></div><div class="firstName"></div><div class="middleName"></div><div class="lastName"></div><div class="company"></div><div class="designation"></div><div class="city"></div><div class="zip"></div><div class="dob"></div><div class="startDate"></div><div class="endDate"></div></div>`
  document.querySelector('.resultSet').insertAdjacentHTML('beforeend', htmlcontent);
}
htmlcontent = `<div class="indexNo"></div><div class="name"></div><div class="firstName"></div><div class="middleName"></div><div class="lastName"></div><div class="company"></div><div class="designation"></div><div class="city"></div><div class="zip"></div><div class="dob"></div><div class="startDate"></div><div class="endDate"></div>`
document.querySelector('.header').insertAdjacentHTML('beforeend', htmlcontent);
htmlcontent = '';

var outputExcel;
var filename;

var headers = [];
var headersoriginal = [];
//----------------FORM----------------------------------
filehandle = document.getElementById('myfile')
openexcel = document.querySelector('.openExcel')
autoMap = document.querySelector('.autoMapping')
saveexcel = document.querySelector('.saveExcel')
inputUploadButton = document.querySelector('.inputUploadButton')
saveMap = document.querySelector('.saveMapping');

openexcel.addEventListener('click', function () {
  filehandle.click();
})

saveexcel.addEventListener('click', function () {
  download(outputExcel);
})

//---------------------AJAX-------------------------------
$(function () {
  $('.autoMapping').click(function () {
    var form_data = new FormData();
    form_data.append('file', $('#myfile').prop('files')[0]);
    $.ajax({
      type: 'POST',
      url: '/uploader',
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      success: function (data) {
        if (data != 'Error') {
          outputExcel = JSON.parse(data);
          //console.log(outputExcel);
          createTable(outputExcel);
          swal("Auto Mapping Complete!", "The columns have been mapped.", "success");
        } else {
          swal("Error!", "An error occurred while mapping.", "error");
        }
      },
    });
  });
});


//----------------------SAVE MAPPING-----------------------
$(function () {
  $('.saveMapping').click(function () {
    data_list = getSelectedOptions();
    var form_data = new FormData();
    form_data.append('file', $('#myfile').prop('files')[0]);
    form_data.append('header', data_list);
    //console.log(form_data);
    $.ajax({
      type: 'POST',
      url: '/savemap',
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      success: function (data) {
        if (data != 'Error') {
          outputExcel = JSON.parse(data);
          //console.log(outputExcel);
          createTable(outputExcel);
          swal("Manual Mapping Complete!", "The columns have been mapped.", "success");
        } else {
          swal("Error!", "An error occurred while mapping.", "error");
        }
      },
    });
  });
});

//----------------MODAL-----------------------------------
var modal = document.getElementById("myModal");
var manualmapping = document.querySelector('.manualMapping');
var mapform = document.querySelector('.mapForm');
var infoblock = document.querySelector('.infoBlock');
var span = document.querySelector('.close');
var floatbtn = document.querySelector('.float');

manualmapping.onclick = function () {
  mapform.style.display = "flex";
  infoblock.style.display = "none"
  modal.style.display = "block";
}

span.onclick = function () {
  modal.style.display = "none";
}

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

floatbtn.onclick = function () {
  mapform.style.display = "none";
  infoblock.style.display = "block"
  modal.style.display = "block";
}

//----------------READING AND DISPAYING EXCEL FILE------------------
var fileUpload = document.getElementById('myfile');

fileUpload.onchange = function (evt) {
  if (typeof (FileReader) != "undefined") {

    var reader = new FileReader();

    //For Browsers other than IE.
    if (reader.readAsBinaryString) {
      reader.onload = function (e) {
        enableButtons();
        ProcessExcel(e.target.result);
      };
      reader.readAsBinaryString(fileUpload.files[0]);
      filename = document.getElementById('myfile').files[0].name.split('.')[0];
      //console.log(filename);
    } else {
      //For IE Browser.
      reader.onload = function (e) {
        var data = "";
        var bytes = new Uint8Array(e.target.result);
        for (var i = 0; i < bytes.byteLength; i++) {
          data += String.fromCharCode(bytes[i]);
        }
        enableButtons();
        ProcessExcel(data);
      };
      reader.readAsArrayBuffer(fileUpload.files[0]);
      filename = document.getElementById('myfile').files[0].name.split('.')[0];
    }
  } else {
    alert("This browser does not support HTML5.");
  }
};

//-------------------------------PROCESS EXCEL-----------------------------------

function ProcessExcel(data) {
  //Read the Excel File data.
  var workbook = XLSX.read(data, {
    type: 'binary'
  });

  var firstSheet = workbook.SheetNames[0];
  var excelRows = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[firstSheet]);
  outputExcel = excelRows
  headersoriginal = [];
  for (var k in excelRows[0]) {
    headersoriginal.push(k)
  }
  createTable(excelRows);
};

//----------------------------AUTOMAP---------------------------------------
function createTable(excelRows) {
  headers = [];
  for (var k in excelRows[0]) {
    headers.push(k)
  }

  var tableHead = document.createElement("div");
  tableHead.className = 'header';

  headers.forEach(function (k) {
    var headerCell = document.createElement("div");
    headerCell.innerHTML = k;
    tableHead.appendChild(headerCell);
  });

  var tableEntry = document.createElement("div");
  tableEntry.className = 'resultSet';

  var numrows = 50;
  if (excelRows.length < numrows) {
    numrows = excelRows.length
  }
  for (var i = 1; i < numrows; i++) {
    var row = document.createElement("div");
    row.className = 'entry'

    headers.forEach(function (k) {
      var headerCell = document.createElement("div");
      headerCell.innerHTML = excelRows[i][k];
      row.appendChild(headerCell);
    });
    tableEntry.appendChild(row)
  }

  var dvExcel = document.querySelector('.container');
  dvExcel.innerHTML = "";
  dvExcel.appendChild(tableHead);
  dvExcel.appendChild(tableEntry);
  swal("Excel Imported!", "Viewing the first 50 rows.", "success");
};

//----------------AUTOMAP-----------------------------------------------------
function readExcel(file) {
  var reader = new FileReader();

  //For Browsers other than IE.
  if (reader.readAsBinaryString) {
    reader.onload = function (e) {
      ProcessExcel(e.target.result);
    };
    reader.readAsBinaryString(file);
  } else {
    //For IE Browser.
    reader.onload = function (e) {
      var data = "";
      var bytes = new Uint8Array(e.target.result);
      for (var i = 0; i < bytes.byteLength; i++) {
        data += String.fromCharCode(bytes[i]);
      }
      ProcessExcel(data);
    };
    reader.readAsArrayBuffer(file);
  }
}


//---------------------------GENERATE SELECT MENU OPTIONS------------------------

manualMap = document.querySelector('.manualMapping')

manualMap.addEventListener('click', function () {
  htmlcontent = ''
  headersoriginal.push('Empty String')
  headersoriginal.forEach(function (k) {
    htmlcontent = htmlcontent + `<option value="${k}">${k}</option>`
  });

  childrenform = Array.from(document.querySelector('.mapForm').children);
  childrenform.forEach(function (k, i) {

    if (k.tagName.toLowerCase() === 'div') {
      k.children[1].innerHTML = '';
      k.children[1].insertAdjacentHTML("beforeend", htmlcontent);
    }
    if (i === 0) {
      k.children[1].insertAdjacentHTML("afterbegin", `<option value="First + Last Name">First + Last Name</option>`);
    }
    if (i === 1 || i == 3) {
      k.children[1].insertAdjacentHTML("afterbegin", `<option value="Get From Name">Get From Name</option>`);
    }
  });
  htmlcontent = ''
  headersoriginal.pop(-1)

});

//----------------GET SELECT MENU OPTIONS----------------------------------------
function getSelectedOptions() {
  var selectedlist = [];
  childrenform = Array.from(document.querySelector('.mapForm').children);
  childrenform.forEach(function (k) {

    if (k.tagName.toLowerCase() === 'div') {
      ele = k.children[1]
      selectedlist.push(ele.options[ele.selectedIndex].value);
    }
  });

  return selectedlist;
}


//-----------------------------MAP MANUALLY--------------------------------------
//saveMap.addEventListener('click', function () {
//  selectedlist =  getSelectedOptions();
//  console.log(selectedlist);
//  })


//-----------------------------DOWNLOAD FILE-------------------------------------


function download(records) {
  var fileName = 'a.xlsx'
  var workSheet = XLSX.utils.json_to_sheet(records);
  //console.log("THis is Worksheet", workSheet);
  var wb = XLSX.utils.book_new();
  //console.log("THis is workbook", wb)
  XLSX.utils.book_append_sheet(wb, workSheet, fileName);

  XLSX.writeFile(wb, 'output_' + filename + '.xlsx', {
    bookType: 'xlsx',
    type: "binary",
    "compression": true
  });
};


function enableButtons() {
  document.querySelector('.autoMapping').disabled = false;
  document.querySelector('.manualMapping').disabled = false;
  document.querySelector('.saveExcel').disabled = false;
  document.querySelector('.autoMapping2').disabled = false;
  document.querySelector('.manualMapping2').disabled = false;
  document.querySelector('.saveExcel2').disabled = false;
}

//------------------------------------SIDE NAV-------------------------------

document.querySelector('.mobNav').addEventListener('click', function (e) {
  openNav();
})

function openNav() {
  document.querySelector(".sidenav").style.width = "300px";
}

document.querySelector('.closebtn').addEventListener('click', function (e) {
  closeNav();
})

function closeNav() {
  document.querySelector(".sidenav").style.width = "0";
}


document.querySelector('.openExcel2').addEventListener('click', function (e) {
  filehandle.click()
})

document.querySelector('.saveExcel2').addEventListener('click', function (e) {
  saveexcel.click();
})

document.querySelector('.autoMapping2').addEventListener('click', function (e) {
  document.querySelector('.autoMapping').click();
})

document.querySelector('.manualMapping2').addEventListener('click', function (e) {
  manualMap.click();
})