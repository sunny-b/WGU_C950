class HashTable
    def initialize(size = 10)
        @map = create_map(size)
    end

    def insert(key, value)
        bucket = find_bucket(key)

        extent = find_kv_pair(key, bucket)

        if extent.empty?
          bucket << [key, value]
        else
          extent[1] = value
        end

        true
    end

    def find(key)
        bucket = find_bucket(key)

        find_kv_pair(key, bucket).last
    end

    private

    attr_accessor :map

    def create_map(size)
        map = []

        size.times { |_| map << [] }

        map
    end

    def find_bucket(key)
        map[key % map.length]
    end

    def find_kv_pair(key, bucket)
      bucket.each do |kv_pair|
        return kv_pair if kv_pair.first == key
      end

      []
    end
end
