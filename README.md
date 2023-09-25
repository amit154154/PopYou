# PopYou!

PopYou! is a project to create custom Funko Pop figures from text and images. With PopYou!, you can bring your favorite characters and ideas to life in the iconic Funko Pop style.
Using Gans and not diffusion, such that the runtime and memory requirements are much lower.


## Method

first I generated 30000 images of funko using the componey deci new diffusion model.
Then I used the dataset to train a GAN model using FastGan and the results are below.

![FastGan examples](/Users/mac/PycharmProjects/PopYou!/assets/fast_gan_examples.jpg)

after that I froze the gan and created an inversion model using frozen clip as backbone,
this gives the inversion model the ability to generate images from text and from images in other domains such as real images of people and faces.


the examples below are generated using the inversion model such that the
text given is "funko pop dull of {name} in a white background".


| Celebrty Name    | PopYou! Model | Different Model                                      |
|------------------|---------------|------------------------------------------------------|
| Barack Obama     | <img src="assets/Barack_Obama_fastgan.png" width="200"> | <img src="assets/Barack_Obama_deci.png" width="200"> |
| Alan Turing      | <img src="assets/Alan_Turing_fastgan.png" width="200"> | <img src="assets/Alan_Turing_deci.png" width="200">  |
| Elsa from frozen | <img src="assets/Elsa_fastgan.png" width="200"> | <img src="assets/Elsa_deci.png" width="200">         |


these are examples using the clip image encoding of a face of the person.

| Celebrty Name           | Image                                                        | PopYou! Model                                                 |
|-------------------------|--------------------------------------------------------------|---------------------------------------------------------------|
| Sun from Lost!          | <img src="assets/sun_Lost_image.webp" width="200">           | <img src="assets/sun_Lost_fastgan.png" width="200">           |
| Bon from Lost!          | <img src="assets/bon_Lost_image.webp" width="200">           | <img src="assets/bon_Lost_fastgan.png" width="200">           |
| Ras from SiliconValley  | <img src="assets/ras_SiliconValley_image.webp" width="200">  | <img src="assets/ras_SiliconValley_fastgan.png" width="200">  |
| Lori from SiliconValley | <img src="assets/lori_SiliconValley_image.jpeg" width="200"> | <img src="assets/lori_SiliconValley_fastgan.png" width="200"> |



## Results

|                 | PopYou! | deci diffusion |
|-----------------|---------|----------------|
| clip similarity | 0.32    | 0.34           |
| Fid             | 562     | 258            |

