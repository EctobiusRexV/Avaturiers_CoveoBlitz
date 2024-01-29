Ce bot a été écrit en Python pour le défi de qualification du Coveo Blitz 2024. Le but est d'optimiser le nombre de points accumulés en 1000 ticks de simulation en tirant sur des astéroides. Les gros astéroides se divisent en deux astéroides médium qui se divisent en trois petits astéroides. Plus ils sont petits, plus ils valent de points.

![](shooting.gif)

Liste d'opimisations:
- Garde une liste d'astéroides tirés afin de seulement le faire une fois.
- Compense les tirs afin de frapper les astéroides même s'ils bougent.
- Ne tire pas sur les astéroides qui vont sortir de la porté de tir.
- Tire sur les plus petits astéroides avant qu'ils apparaissent.
- Priorise les astéroides les plus loins afin d'avoir le temps de tous les tirer.
