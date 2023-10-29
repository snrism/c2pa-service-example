# c2patool Python service example 

This repository is forked from [Node.js](https://github.com/contentauth/c2pa-service-example) implementation and has the Python equivalent server implementation. The functionalityy remains the same and allows users to upload images and add a C2PA manifest to each image.

## Install and build

Follow these steps:

1. Clone this repo by entering this command in a terminal window:
    ```
    git clone https://github.com/snrism/c2pa_service_example.git
    ```
1. Download the latest version of c2patool for your platform from <https://github.com/contentauth/c2patool/releases>.
1. Extract the zip file and put a copy of the `c2patool` executable in the root of this repo (`c2pa_service_example` directory).  NOTE: Depending on your operating system, you may need to take some extra steps to be able to run this file; for example on MacOS you have to [follow the instructions to open a Mac app from an unidentified developer](https://support.apple.com/guide/mac-help/open-a-mac-app-from-an-unidentified-developer-mh40616/mac).  
1. Open a terminal window and install the required packages. Enter these commands
    ```
    cd <path_where_you_cloned_repo>/c2pa_service_example
    npm install
    ```
1. Start the service by entering this command:
    ```
    python3 server.py
    ```
    You'll see this in your terminal:
    ```
    * Serving Flask app 'server'
    * Debug mode: on
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on http://127.0.0.1:8000
    Press CTRL+C to quit
    * Restarting with stat
    * Debugger is active!
    ```

## Add C2PA manifest to any PNG or JPEG files. 

1. Open a browser to <http://localhost:8000>.
1. Click the **Choose Files** button and select one or more JPEG or PNG images in the native file chooser dialog. 
    <br/>The service uploads the selected images, stores them in the `uploads` folder, and then calls the c2patool to add a C2PA manifest to each image. 
3. Hover over the badge for information about the associated manifest.
4. The service returns the full-sized image, not thumbnails.
5. Right-click and download an image to view the credentials on <https://verify.contentauthenticity.org/>.

### Overview of the app

The code in `server.py` (re-write of server.js) contains all the server-side logic.  It defines three routes:
- GET `/version` displays the version of c2patool being used
- POST `/upload` uploads a file, adds a C2PA manifest, and returns a URL.
- GET `/`, the default route, serves `client/index.html`, which is a simple page with a user interface you can use to upload one or more files.  The associated client JavaScript is in [`client/index.js`](https://github.com/contentauth/c2pa_service_example/blob/main/client/index.js).  Selecting files triggers a [client JavaScript event listener](https://github.com/contentauth/c2pa_service_example/blob/main/client/index.js#L89) that calls the `/upload` route for each file and then calls the [`addGalleryItem`](https://github.com/contentauth/c2pa_service_example/blob/main/client/index.js#L19) function to display the returned image on the page.

## Customizing

The data added to the manifest is determined by the `manifest.json` file in the root folder. To modify the information added to the file, modify `manifest.json`.

For more information about c2patool and manifests, see [the documentation](https://opensource.contentauthenticity.org/docs/c2patool/).




