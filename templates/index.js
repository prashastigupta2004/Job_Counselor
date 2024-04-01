// document.addEventListener('DOMContentLoaded', function() {
//     // Function to create job listing box
//     function createJobListing(url) {
//         // Create elements for job listing box
//         var jobBox = document.createElement('div');
//         jobBox.classList.add('card', 'mb-3');
//         var jobBoxBody = document.createElement('div');
//         jobBoxBody.classList.add('card-body');
//         var jobTitle = document.createElement('h5');
//         jobTitle.classList.add('card-title');
//         jobTitle.textContent = 'Job Role: Sample Job Role';
//         var jobLocation = document.createElement('p');
//         jobLocation.classList.add('card-text');
//         jobLocation.textContent = 'Location: Sample Location';
//         var applyButton = document.createElement('a');
//         applyButton.classList.add('btn', 'btn-primary', 'mr-2');
//         applyButton.setAttribute('href', url);
//         applyButton.setAttribute('target', '_blank');
//         applyButton.textContent = 'Apply';
//         var saveButton = document.createElement('button');
//         saveButton.classList.add('btn', 'btn-secondary');
//         saveButton.textContent = 'Save Job';
        
//         // Append elements to job listing box
//         jobBoxBody.appendChild(jobTitle);
//         jobBoxBody.appendChild(jobLocation);
//         jobBoxBody.appendChild(applyButton);
//         jobBoxBody.appendChild(saveButton);
//         jobBox.appendChild(jobBoxBody);
        
//         // Append job listing box to container
//         document.getElementById('jobListingContainer').appendChild(jobBox);
//     }

//     // Get matching URLs from Flask backend
//     var matchingUrls = {{ matching_urls | tojson }};

//     // Create job listing boxes for each URL
//     matchingUrls.forEach(function(url) {
//         createJobListing(url);
//     });
// });