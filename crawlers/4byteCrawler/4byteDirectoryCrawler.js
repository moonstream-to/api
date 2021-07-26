const fetch = require('node-fetch')
const fs = require("fs")

   
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function makeRequest(url, sleepTime) {
    if (sleepTime)
        sleep(sleepTime)
    let response = await fetch(url);
    let json = await response.json();
    return json;
}

async function crawlFunctionSignatures() {
    let url = "https://www.4byte.directory/api/v1/signatures/";
    let response = await makeRequest(url)
    let signatures = response.results;
    while (response.next) {
        response = await makeRequest(response.next)
        signatures = signatures.concat(response.results)
        console.log(`already crawled : ${signatures.length}`)
    }
    fs.writeFileSync("function_signatures.json", JSON.stringify(signatures))
}

async function crawlEventSignatures() {
    let url = "https://www.4byte.directory/api/v1/event-signatures/";
    let response = await makeRequest(url)
    let signatures = response.results;
    while (response.next) {
        response = await makeRequest(response.next)
        signatures = signatures.concat(response.results)
        console.log(`already crawled : ${signatures.length}`)
    }
    fs.writeFileSync("event_signatures.json", JSON.stringify(signatures))
}

//crawlFunctionSignatures()
//crawlEventSignatures();
