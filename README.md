# gmaps-scraping
A simple Google maps scraping app made with Selenium.

# Prior requirements
-Python3
-Selenium
-Chrome

# Informations

<ins>Usage</ins>
Just import the main() function from the file or paste the function inside a file.
There is no need to compile.

<ins>Arguments</ins>
The function needs two arguments; keyword and location.
How the function works is that it first searches the location then the keyword.
This leads to faster results but less accurate ones.
It is generally recommended to use coordinates in location as it may make things more accurate.
However, if there is no result near the location; unexpected responses may occur

<ins>Configs</ins>
Delay = How many seconds to wait for a page to load.
(I recommend using 3-5)

<ins>Description of each data scraped</ins>
nama_tempat = Is taken by using a css selector, we looked for a h1 with the class of "DUwDvf.lfPIob" and scraped the text from it
alamat = Is taken by using a css selector, we looked for a button with the data-item-id of "address" and then we scrape the aria label from it
website = Is taken by using a css selector, we looked for an anchor tag with the data-item-id of "authority" and then extracted the aria label from it.
no_telp = Is taken by searching for elements with the class "CsEnBe" and filtering for those with the data-item-id containing "phone:tel:". We then extract the aria label from the relevant element.
rating = Is taken by using a css selector, we found a span with the class "ceNzKf" and obtained the aria label containing the rating information.
jadwal = Is obtained by searching for elements with the class "mxowUb" which represent the opening hours. We loop through these elements and associate each day with its corresponding opening hours.

# Example Usage
```python
# Example usage of the main function
keyword = "restaurant"
coordinates = "latitude, longitude"  # Replace with actual coordinates
result = main(keyword, coordinates)
```
print(result)
