const sqlite3 = require('sqlite3').verbose()
const fs = require('fs')
let db = new sqlite3.Database('./signatures.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
      console.error(err.message);
    }
    
});

function put_func_signatures_to_db() {
    db.serialize(() => {
        db.run('create table if not exists '
            + 'function_signatures('
            + 'id numeric primary key,'
            + 'text_signature text,'
            + 'hex_signature text)')
        
        let stmt = db.prepare('insert into function_signatures values (?, ?, ?)')
        let function_signatures = JSON.parse(fs.readFileSync("./function_signatures.json"))
        function_signatures.forEach((item) => {
            try {
                stmt.run([item.id, item.text_signature, item.hex_signature])
                
            }
            catch(err) {
                console.log(item)
                console.log(err)
            }
        })
    })
}

function put_event_signatures_to_db() {
    db.serialize(() => {
        db.run('create table if not exists '
            + 'event_signatures('
            + 'id numeric primary key,'
            + 'text_signature text,'
            + 'hex_signature text)')
        
        let stmt = db.prepare('insert into event_signatures values (?, ?, ?)')
        let function_signatures = JSON.parse(fs.readFileSync("./event_signatures.json"))
        function_signatures.forEach((item) => {
            try {
                stmt.run([item.id, item.text_signature, item.hex_signature])
                
            }
            catch(err) {
                console.log(item)
                console.log(err)
            }
        })
    })
}

//put_func_signatures_to_db()
//put_event_signatures_to_db()