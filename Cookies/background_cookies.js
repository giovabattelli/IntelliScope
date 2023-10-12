// Specify the details of the cookie you want to retrieve
const cookieDetails = {
    url: "https://www.gradescope.com/courses/567436/assignments/3290069/submissions/193710547/select_pages", // Replace with the website URL
    name: "signed_token",  // Replace with the name of the cookie you want
  };
  
  // Get the cookie
  chrome.cookies.get(cookieDetails, (cookie) => {
    if (cookie) {
      console.log("Cookie found:", cookie);
    } else {
      console.log("Cookie not found.");``
    }
  });
  