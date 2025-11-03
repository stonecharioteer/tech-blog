module One
  class Fred
    def greet
      "Hello from Fred the class!"
    end
  end

  def self.use_fred_symbol
    # Use the symbol :Fred to get the class
    klass = const_get(:Fred)
    instance = klass.new
    puts "In module One, using symbol :Fred to get the class"
    puts "const_get(:Fred) returns: #{klass.class}"
    puts "Creating instance: #{instance.greet}"
    :Fred  # Return the symbol
  end
end

module Two
  Fred = 42  # Fred is a constant

  def self.use_fred_symbol
    # Use the symbol :Fred to get the constant
    value = const_get(:Fred)
    result = value * 2
    puts "In module Two, using symbol :Fred to get the constant"
    puts "const_get(:Fred) returns: #{value.class} with value #{value}"
    puts "Calculating #{value} * 2 = #{result}"
    :Fred  # Return the symbol
  end
end

module Three
  def self.Fred()  # Fred is a method
    "I'm the Fred method!"
  end

  def self.use_fred_symbol
    # Use the symbol :Fred to call the method
    result = send(:Fred)
    puts "In module Three, using symbol :Fred to call the method"
    puts "send(:Fred) returns: #{result}"
    :Fred  # Return the symbol
  end
end

puts "=== Using the symbol :Fred in different contexts ==="
puts
sym1 = One.use_fred_symbol
puts "Returned symbol object_id: #{sym1.object_id}"
puts

sym2 = Two.use_fred_symbol
puts "Returned symbol object_id: #{sym2.object_id}"
puts

sym3 = Three.use_fred_symbol
puts "Returned symbol object_id: #{sym3.object_id}"
puts

puts "=== The symbol :Fred is the same everywhere ==="
puts "All three object_ids match: #{sym1.object_id == sym2.object_id && sym2.object_id == sym3.object_id}"
puts "sym1.equal?(sym2): #{sym1.equal?(sym2)}"
puts "sym2.equal?(sym3): #{sym2.equal?(sym3)}"
