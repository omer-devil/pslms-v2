(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    // Initiate the wowjs
    new WOW().init();

    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').css('top', '0px');
        } else {
            $('.sticky-top').css('top', '-100px');
        }
    });
    
    // Dropdown on mouse hover
    const $dropdown = $(".dropdown");
    const $dropdownToggle = $(".dropdown-toggle");
    const $dropdownMenu = $(".dropdown-menu");
    const showClass = "show";
    
    $(window).on("load resize", function() {
        if (this.matchMedia("(min-width: 992px)").matches) {
            $dropdown.hover(
            function() {
                const $this = $(this);
                $this.addClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "true");
                $this.find($dropdownMenu).addClass(showClass);
            },
            function() {
                const $this = $(this);
                $this.removeClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "false");
                $this.find($dropdownMenu).removeClass(showClass);
            }
            );
        } else {
            $dropdown.off("mouseenter mouseleave");
        }
    });

    // Image display for teacher and student registration
    const uploadInput = document.getElementById('uploadInput');
    const imagePreview = document.getElementById('imagePreview');

    if (uploadInput && imagePreview) {
        uploadInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    imagePreview.innerHTML = '<img src="' + event.target.result + '" alt="Uploaded Image">';
                };
                reader.readAsDataURL(file);
            } else {
                imagePreview.innerHTML = '';
            }
        });
    }

    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });

    // Header carousel
    $(".header-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        items: 1,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });

    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        margin: 24,
        dots: true,
        loop: true,
        nav : false,
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });
})(jQuery);

//admin dashboard cound student and teacher

document.addEventListener('DOMContentLoaded', function () {
    fetch('http://localhost:3000/students/count') // Adjust the URL as needed
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const studentCount = data.count; // Get the count of students

            // Create a bar chart to display the student count
            const ctx = document.getElementById('chart').getContext('2d');
            new Chart(ctx, {
                type: 'bar', // You can also use 'doughnut', 'line', etc.
                data: {
                    labels: ['Students'],
                    datasets: [{
                        label: 'Count',
                        data: [studentCount],
                        backgroundColor: ['rgba(75, 192, 192, 0.6)'],
                        borderColor: ['rgba(75, 192, 192, 1)'],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // You can modify the chart type and appearance as needed
        })
        .catch(error => {
            console.error('Error fetching student count:', error);
        });
});


//fetch code for Teacher
document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('teacher-table-body');

    fetch('http://localhost:3000/teacher/getAllTeacher')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Loop through the fetched data
            data.forEach(teacher => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    
                    <td>${teacher.teacherID}</td>
                    <td>${teacher.firstName + " " +teacher.secondName+ " " +teacher.lastName}</td>
                    <td>${teacher.profession}</td>
                    <td>${teacher.gender}</td>


                    <td>
                        <button type="button" class="btn btn-primary btn-sm edit-btn" data-course-id="${teacher._id}">Edit</button>
                        <button type="button" class="btn btn-danger btn-sm delete-btn">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});



//fetch code for Student
document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('student-table-body');

    fetch('http://localhost:3000/student/getAllStudents')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Loop through the fetched data
            data.forEach(student => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    
                    <td>${student.studentID}</td>
                    <td>${student.firstName + " " +student.secondName+ " " +student.lastName}</td>
                    <td>${student.grade}</td>
                    <td>${student.gender}</td>

                    <td>
                        <button type="button" class="btn btn-primary btn-sm edit-btn" data-course-id="${student._id}">Edit</button>
                        <button type="button" class="btn btn-danger btn-sm delete-btn">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});


//fetch code course

document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('course-table-body');

    

    
    fetch('http://localhost:3000/data/getAllCourses')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            data.forEach(course => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${course.course_name}</td>
                    <td>${course.course_description}</td>
                    <td>
                        <button type="button" class="btn btn-primary btn-sm edit-btn" data-course-id="${course._id}">Edit</button>
                        <button type="button" class="btn btn-danger btn-sm delete-btn">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});


//fetch code course

document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('student-course-table-body');

    

    
    fetch('http://localhost:3000/data/getAllCourses')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            data.forEach(course => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${course.course_name}</td>
                    <td>${course.course_description}</td>
                    
                `;
                tableBody.appendChild(row);
            });

        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});

//fetch code for Student
document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('teacher-student-table-body');

    fetch('http://localhost:3000/student/getAllStudents')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Loop through the fetched data
            data.forEach(student => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    
                    <td>${student.firstName + " " +student.secondName+ " " +student.lastName}</td>
                    <td>${student.grade}</td>
                    <td>${student.gender}</td> 
                    
                    `;
                tableBody.appendChild(row);
            });

        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});


//assesment review teacher 
document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('assessment-table-body');

    fetch('http://localhost:3000/assessment/getAllAssessments') 
        .then(response => response.json())
        .then(data => {
            data.forEach(assessment => {
                const row = document.createElement('tr');

                // Calculate the total score based on the weighted percentages
                const totalScore = (assessment.test1) + (assessment.test2 ) + (assessment.midExam ) + (assessment.finalExam );

                row.innerHTML = `
                    <td>${assessment.studentID}</td>
                    <td>${assessment.subject}</td>
                    <td>${assessment.test1}</td>
                    <td>${assessment.test2}</td>
                    <td>${assessment.midExam}</td>
                    <td>${assessment.finalExam}</td>
                    <td>${totalScore.toFixed(2)}</td>
                `;
                
                // Append the row to the table body
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching assessment data:', error);
        });
});


//assesment review student 
document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('grade-table-body');

    fetch('http://localhost:3000/assessment/getAllAssessments') 
        .then(response => response.json())
        .then(data => {
            data.forEach(assessment => {
                const row = document.createElement('tr');

                // Calculate the total score based on the weighted percentages
                const totalScore = (assessment.test1) + (assessment.test2 ) + (assessment.midExam ) + (assessment.finalExam );

                row.innerHTML = `
                    <td>${assessment.studentID}</td>
                    <td>${assessment.subject}</td>
                    <td>${assessment.test1}</td>
                    <td>${assessment.test2}</td>
                    <td>${assessment.midExam}</td>
                    <td>${assessment.finalExam}</td>
                    <td>${totalScore.toFixed(2)}</td>
                `;
                
                // Append the row to the table body
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching assessment data:', error);
        });
});

// Set the current date as the default value of the date input field in the attendance form
document.addEventListener('DOMContentLoaded', function () {
    // Find the date input element in the attendance form
    const dateInput = document.querySelector('#attendance-form input[name="date"]');
    
    // Get the current date in YYYY-MM-DD format
    const today = new Date().toISOString().split('T')[0];
    
    // Set the value of the date input field to the current date
    if (dateInput) {
        dateInput.value = today;
    }
});

// feach attendance for teacher
document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('attendance-table-body');

    // Fetch all attendance records from the server
    fetch('http://localhost:3000/attendance/getAllAttendance')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Clear existing rows from the table
            tableBody.innerHTML = '';

            // Loop through the fetched data
            data.forEach(attendance => {
                // Create a row for each attendance record
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${attendance.studentID}</td>
                    <td>${attendance.subjectPeriod}</td>
                    <td>${new Date(attendance.date).toLocaleDateString()}</td>
                    <td>${attendance.grade}</td>
                    <td>${attendance.attendanceStatus}</td>
                `;
                
                // Append the row to the table body
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching attendance data:', error);
        });
});


// login session

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');
    
    form.addEventListener('submit', function(event) {
        // Prevent the form from submitting traditionally
        event.preventDefault();
        
        // Get the entered username and password
        const name = document.getElementById('name').value;
        const password = document.getElementById('password').value;
        
        // Redirect based on the username and password combinations
        if (name === 'stud' && password === '123') {
            // Redirect to student dashboard
            window.location.href = 'stud_dash.htm';
        } else if (name === 'teach' && password === '123') {
            // Redirect to teacher dashboard
            window.location.href = 'teach_dash.htm';
        } else if (name === 'admin' && password === '123') {
            // Redirect to admin dashboard
            window.location.href = 'admin_dash.htm';
        } else {
            // Show an alert if the credentials are invalid
            alert('Invalid credentials. Please try again.');
        }
    });
});





// Function for login button
function goBack() {
    window.location.href = 'index.html'; // Redirect to index.html
}
