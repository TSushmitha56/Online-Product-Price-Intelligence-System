from rest_framework import serializers
from .models import PriceAlert, SearchHistory, Wishlist, PriceHistory


class PriceAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceAlert
        fields = ('id', 'product_name', 'target_price', 'current_price', 'product_url', 'created_at', 'status')
        read_only_fields = ('id', 'current_price', 'created_at')

    def create(self, validated_data):
        user = self.context['request'].user
        return PriceAlert.objects.create(user=user, **validated_data)


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ('id', 'query', 'timestamp')
        read_only_fields = ('id', 'timestamp')

    def create(self, validated_data):
        user = self.context['request'].user
        return SearchHistory.objects.create(user=user, **validated_data)


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id', 'product_name', 'store', 'price', 'product_url', 'image_url', 'added_at')
        read_only_fields = ('id', 'added_at')

    def create(self, validated_data):
        user = self.context['request'].user
        # get_or_create to prevent duplication by product_url (empty url = allow multiple)
        product_url = validated_data.get('product_url', '')
        if product_url:
            obj, _ = Wishlist.objects.get_or_create(
                user=user,
                product_url=product_url,
                defaults=validated_data
            )
            return obj
        return Wishlist.objects.create(user=user, **validated_data)


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ('id', 'product_name', 'store', 'price', 'timestamp')
        read_only_fields = ('id', 'timestamp')
