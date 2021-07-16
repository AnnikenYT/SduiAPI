class httpWrapper {

    constructor(tableId, token, fileHandler, delta=0) {

        this.tableId=tableId;
        this.token=token;
        this.fileHandler = fileHandler;

    }

    static httpGet(theUrl, header=null)
        {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", theUrl, false ); // false for synchronous request

            if (header != null) {
                xmlHttp.setRequestHeader("authorization",this.token);
                xmlHttp.setRequestHeader("user-agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            }

            xmlHttp.send( null );
            return xmlHttp.responseText;
        }

    static unix2dt(ts) {
        var date = new Date(ts * 1000);
        // Hours part from the timestamp
        var hours = date.getHours();
        // Minutes part from the timestamp
        var minutes = "0" + date.getMinutes();
        // Seconds part from the timestamp
        var seconds = "0" + date.getSeconds();
        var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

        return formattedTime;
    }

    static getData() {

        file = this.httpGet(this.fileHandler+"?action=read&filename=LAST_DOWNLOAD");
        

        console.log("Data too old, downloading new data.");


    }

}