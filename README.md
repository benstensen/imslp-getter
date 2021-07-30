<h1>IMSLP Getter</h1>
<p>This program is designed to get URLs to PDFs from IMSLP.org based on user input. The process is typically more streamlined than manual navigation through the website, and skips website-imposed waittimes to retrieve some desired link much faster.</p>
<h2>How It Works</h2>
<ol>
  <li>The user inputs a search term.</li>
  <li>The program fetches the Google search page corresponding to the search term, and displays relevant results to the user.</li>
  <li>The user selects from the displayed results, and the program generates the corresponding URL for IMSLP.org.</li>
  <li>The program fetches the IMSLP page and asks the user for a part to search for.</li>
  <li>The program displays the relevant results, or asks for a different search term if no parts matched.</li>
  <li>The user selects from the results, and the program traverses IMSLP until it reaches the PDF link.</li>
  <li>The PDF link is returned to the user.</li>
</ol>
<h2>Todo</h2>
<ul>
  <li>Optimize currently existing code 
    <ul>
      <li>Rewrite for greater efficiency + better compliance with good Python programming practices</li>
      <li>Add more robust error-handling to decrease risk of program failure</li>
      <li>Test more to improve Crawler module</li>
    </ul>
  </li>
  <li>Refactor code to allow fetching multiple links in one execution</li>
  <li>Implement GUI-driven experience as a web app with Django</li> 
</ul>

<h2>Why does this exist?</h2>

<p>I'm an avid musician, and I frequently find myself using the services offered by the International Music Score Library Project (IMSLP) / Petrucci Music Library (PML). One key element of the experience for me is waiting the dreaded 15 seconds before the PDF link is actually made accessible. One day, I found that the link is available in the page source immediately upon loading the page, which gave me the idea to automate the bypassing process. What I'm trying to create is a much easier way to fetch links to the sheet music I want to play, without needing to navigate the website manually.</p>
