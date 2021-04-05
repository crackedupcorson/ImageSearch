# ImageSearch

## Description
This was my final year project for university. It took a theory where a bulk image search and comparison could be used to give an semi-accurate attempt on where the image was taken. The code built attempts to execute on that theory.

It has since been refactored a little bit and cleaned up for Python3, and some OpenCV changes were made, but it remains mostly untouched.
Who knows, maybe I'll contribute to it again soon.

## How does it work?
It follows this flow

- The user uploads an image, and provides an estimated location
- A bulk image search is then made to find geotagged images that roughly match the search criteria 
- Currently Flickr is the only data source, but I hope add more in the future
- It then runs a feature matching algorithm on the returned images
- It then runs a colour histogram comparison on the returned images

## Technologies and Libs Used

- python requests for API requests to datasources
- the flickr API 
- various python numerical libs
- opencv 3.0

## Future Improvements

The improves I'd like to add in the future are

- multiple data sources to get better sources for edge cases
- better search algorithms (or use a mixture and use a knowledge-based system to determine the correct mixture of feature matchers and colour analysers)
- introduce a messaging system to facilitate the above in an async manner 
- build up a record of previous successes to help in future queries
