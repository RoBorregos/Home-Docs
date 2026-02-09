# Welcome to RoBorregos @Home

<script src="https://kit.fontawesome.com/db131c0a32.js" crossorigin="anonymous"></script>

Welcome to the @Home competition documentation of [RoBorregos](https://roborregos.com), Robotics Representative Team of [Tecnológico de Monterrey](https://tec.mx). This documentation serves as a guide for our project, which focuses on researching and developing a multiproposal modular service robot for the [RoboCup@Home](https://athome.robocup.org/) competition. Our goal is to create a comprehensive software architecture that enables robots to perform various tasks that humans typically handle on a daily basis and adapting this software architecture in affordable hardware.

<p align="center">
  <img src="/assets/landing/TeamPicture.jpeg" alt="RoBorregos Logo">
</p>

## About the Competition

The RoboCup@Home league is the largest annual competition for autonomous service robots. It aims to develop service and assistive robot technology for future domestic applications. The competition evaluates robots' abilities in a realistic home environment through benchmark tests.

<div id="carousel" class="carousel">
  <div class="carousel-item active">
    <img src="/assets/mpPose.jpg" alt="Robot mmpose">
  </div>
  <div class="carousel-item">
    <img src="/assets/home/ObjectDetection/Yolov5DetectionSample.png" alt="Detection">
  </div>
  <div class="carousel-item">
    <img src="/assets/home/HRI/Display.png" alt="Robot Display">
  </div>
  <a class="carousel-control-prev" onclick="prevSlide()">&#10094;</a>
  <a class="carousel-control-next" onclick="nextSlide()">&#10095;</a>
</div>

<style>
.carousel {
  position: relative;
  max-width: 100%;
  margin: auto;
  overflow: hidden;
}

.carousel-item {
  display: none;
  text-align: center;
}

.carousel-item.active {
  display: block;
}

.carousel img {
  width: 400px;
  height: 300px; 
  object-fit: cover; 
  border-radius: 15px; 
}

.carousel-control-prev, .carousel-control-next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 2em;
  color: black;
  cursor: pointer;
  user-select: none;
}

.carousel-control-prev {
  left: 10px;
}

.carousel-control-next {
  right: 10px;
}
</style>

<script>
let currentSlide = 0;
const slides = document.querySelectorAll('.carousel-item');

function showSlide(index) {
  slides[currentSlide].classList.remove('active');
  currentSlide = (index + slides.length) % slides.length;
  slides[currentSlide].classList.add('active');
}

function nextSlide() {
  showSlide(currentSlide + 1);
}

function prevSlide() {
  showSlide(currentSlide - 1);
}

document.addEventListener('DOMContentLoaded', () => {
  showSlide(currentSlide);
});
</script>

## Explore Our Work

<details>
  <summary>Achievements from 2024</summary>
  <ul>
    <li><a href="2024/">Achievements from 2024</a></li>
  </ul>
</details>

<details>
  <summary>Achievements from 2023</summary>
  <ul>
    <li><a href="2023/">2023</a></li>
  </ul>
</details>

<details>
  <summary>Prior achievements</summary>
  <ul>
    <li><a href="2022/">2022 - Jun 2023</a></li>
  </ul>
</details>

<details>
  <summary>Videos of our robot</summary>
  <ul>
    <li><a href="Overview/Media/">Media</a></li>
  </ul>
</details>

## Sections

This project is divided into several sections, each focusing on a specific aspect of the competition and the history of our team. The sections are as follows:

- [Project structure](/Overview/Project%20Structure.md): Provides an overview of the structure managed in the project. And how we are organized to achieve several tasks.
- [Publications](/publications/index.md): Academic papers and research work by our team members.
- [Areas](/Areas/index.md): Describes the main software and hardware modules develop by the team to achive the functionalities in the robot.
- [Team Members](/Team.md): Lists the team members and their roles in the project.
- [2024](/2024/index.md)
- [2023](/2023/index.md)
- [2022](/2022/index.md)

## Contributing

Feel free to contribute to this documentation by submitting a pull request. If you have any questions or suggestions, please contact us.

## Contact Us

If you have any questions, suggestions, or feedback, please feel free to reach out to us. We hope you find our documentation helpful and wish you success in exploring and utilizing our software modules for the RoboCup@Home competition.

<div class="social-icons">
  <a href="https://www.facebook.com/roborregos" target="_blank"><i class="fab fa-facebook"></i></a>
  <i class="fa-brands fa-facebook"></i>
  <a href="https://twitter.com/roborregos" target="_blank"><i class="fab fa-twitter"></i></a>
  <a href="https://www.instagram.com/roborregos" target="_blank"><i class="fab fa-instagram"></i></a>
  <a href="https://www.linkedin.com/company/roborregos" target="_blank"><i class="fab fa-linkedin"></i></a>
</div>

We hope you find our documentation helpful, and we wish you success in exploring and utilizing our software modules for the RoboCup@Home competition.

If you want to see more of our projects, checkout our [GitHub](https://github.com/RoBorregos)