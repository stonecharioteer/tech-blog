def main
  fruits = %w[apple orange kiwi mango banana]
  fruit_lambda = lambda do |fruit|
    puts "I like to eat #{fruit}" unless fruit == 'kiwi'
    fruit if fruit == 'kiwi'
  end
  fruits.each(&fruit_lambda)
  puts "I've processed all the fruits"
end
fave_fruit = main
puts "I love #{fave_fruit}!" unless fave_fruit.nil?
