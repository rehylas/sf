/**
 * Created on 2018/4/26
 * @fileoverview 请填写简要的文件说明.
 * @author westwood (Chen Hua)
 */
const compression = require('compression');
const express = require('express');
const path = require('path');

const app = express();

app.use(compression());

var request = require('request');
var fs = require('fs');
var bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
 
app.get('/', function (req, res) {

    res.sendFile("./dist/index.html" );
 
});

app.use('/', express.static('./dist'));
app.use(express.static("./dist/static"));

 

app.listen('80', function () {
    console.log(`app listening on port 80`)
});

process.on('uncaughtException', (err) => {
    console.error(new Date(), new Error(err));
})

process.on('rejectionHandled', (err) => {
    console.error(new Date(), new Error(err));
})