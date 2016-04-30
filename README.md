<p align="center">
  <br />
  <img src="https://raw.githubusercontent.com/mannynotfound/crying-jordan/master/crying-jordan.jpg" />
</p>

# crying-jordan.io

The streets need this

## inspo

* [Switching Faces With Python](http://matthewearl.github.io/2015/07/28/switching-eds-with-python/)

## usage

#### crying jordan

To get an automated crying jordan, simply tweet an image with a suitable face.

`@username [image]`


Additionally, you can tweet a quoted status that contains images.

`@username [link to tweet]`

#### face swap

To perform face swap between a base image and a source image, tweet as such:

`@username [base image] [source image]`

This will impose the face from the source image onto the base image.

## environment variables

you'll need these system environment variables 

Variable | Description
:------- | :----------
CKEY | Twitter consumer token
CSECRET | Twitter consumer token secret
ATOKEN | Twitter access token
ASECRET | Twitter access token secret
USERID | Twitter user id to track mentions

## todos:

* understand face swap code
* detect face in the wrong direction and automatically mirror horizontally

_note:_

you will need a `landmarks/` directory with the extracted .dat from [this download](http://sourceforge.net/projects/dclib/files/dlib/v18.10/shape_predictor_68_face_landmarks.dat.bz2)

