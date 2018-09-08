(define (domain nosliw)
  (:requirements :strips :typing)
  (:types
    location atl - object
    agent item - atl
    hero dragon wizard - agent
    sorceress - wizard
    sword pen diamond - item
    mountain cave town - location
    )
  (:predicates  (at ?a - atl  ?x - location)
                    (strong ?c - hero) (asleep ?dragon - dragon)
                    (safe ?h - town) (dead ?dragon - dragon)
                    (different ?d - diamond ?d0 - diamond)
                    (possesses ?b - agent ?item - item)
                    (path-from-to ?x - location ?y - location))

  (:action travel
	     :parameters (?a - hero ?x - location ?y - location)
	     :precondition (and (at ?a ?x)
	                        (path-from-to ?x ?y))
	     :effect (and (at ?a ?y)
	                    (not (at ?a ?x))))

  (:action trade
	     :parameters (?a - agent ?b - agent ?x - location ?item - item ?item0 - item)
	     :precondition (and (at ?a ?x)
	                        (at ?b ?x)
	                        (possesses ?a ?item)
	                        (possesses ?b ?item0))
	     :effect (and (not (possesses ?a ?item))
	                    (possesses ?a ?item0)
	                    (not (possesses ?b ?item0))
	                    (possesses ?b ?item)))

  (:action pickup
      :parameters (?a - hero ?x - location ?item - item)
      :precondition (and (at ?item ?x)
                         (at ?a ?x))
      :effect (and (not (at ?item ?x)) (possesses ?a ?item)))


  (:action drop
      :parameters (?a - hero ?x - location ?item - item)
      :precondition (and (possesses ?a ?item)
                         (at ?a ?x))
      :effect (and (not (possesses ?a ?item)) (at ?item ?x)))

  (:action magic
      :parameters (?a - hero ?b - wizard ?x - location ?d - diamond ?d0 - diamond ?d1 - diamond)
      :precondition (and (possesses ?a ?d) (possesses ?a ?d0) (possesses ?a ?d1)
                         (different ?d ?d0) (different ?d ?d1) (different ?d0 ?d1)
                         (at ?a ?x)
                         (at ?b ?x))
      :effect (and (possesses ?b ?d0) (possesses ?b ?d1) (possesses ?b ?d) (strong ?a)
                (not (possesses ?a ?d0)) (not (possesses ?a ?d1)) (not (possesses ?a ?d))))



  (:action song
      :parameters (?a - hero ?b - dragon ?s - town ?pen - pen)
      :precondition  (and (possesses ?a ?pen) (not (dead ?b)))
      :effect (and (asleep ?b) (safe ?s)))

  (:action slaying
      :parameters (?a - hero ?b - dragon ?s - town ?x - location ?sword - sword)
      :precondition  (and (strong ?a) (possesses ?a ?sword)
                            (at ?a ?x) (at ?b ?x))
      :effect (and (dead ?b) (safe ?s) (not (asleep ?b))))
)


