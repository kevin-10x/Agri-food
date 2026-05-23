import React, { useState } from 'react';
import {
  View,
  Text,
  Button,
  Image,
  StyleSheet,
  ActivityIndicator,
  Alert,
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';

const API_BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export default function App() {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const pickImage = async () => {
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (!permission.granted) {
      Alert.alert('Permission required', 'Allow access to photos to use CropMind AI.');
      return;
    }

    const pickerResult = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: [ImagePicker.MediaType.Image],
      quality: 1,
    });

    if (!pickerResult.canceled) {
      setImage(pickerResult.assets[0].uri);
      setResult(null);
    }
  };

  const analyzeCrop = async () => {
    if (!image) {
      Alert.alert('No image selected', 'Please choose a crop image first.');
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', {
        uri: image,
        name: 'crop-image.jpg',
        type: 'image/jpeg',
      });

      const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const confidence =
        typeof response.data.confidence === 'number'
          ? `${response.data.confidence.toFixed(1)}%`
          : response.data.confidence;

      setResult({
        disease: response.data.disease,
        confidence,
        advice: response.data.advice,
      });
    } catch (error) {
      setResult({
        disease: 'Demo Result',
        confidence: '92%',
        advice: 'Backend unavailable. Using fallback advice: remove infected leaves and apply copper-based fungicide.',
      });
    }

    setLoading(false);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🌿 CropMind AI</Text>
      <Text style={styles.subtitle}>Detect crop diseases instantly</Text>
      <Text style={styles.note}>API: {API_BASE_URL}</Text>

      <View style={styles.buttonRow}>
        <Button title="Pick Crop Image" onPress={pickImage} />
      </View>

      {image && <Image source={{ uri: image }} style={styles.image} />}

      <View style={styles.buttonRow}>
        <Button title="Analyze Crop" onPress={analyzeCrop} />
      </View>

      {loading && <ActivityIndicator size="large" color="green" />}

      {result && (
        <View style={styles.resultBox}>
          <Text style={styles.resultText}>🦠 Disease: {result.disease}</Text>
          <Text style={styles.resultText}>📊 Confidence: {result.confidence}</Text>
          <Text style={styles.resultText}>💡 Advice: {result.advice}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
    backgroundColor: '#f5fff5',
  },
  title: {
    fontSize: 30,
    fontWeight: 'bold',
    color: 'green',
    textAlign: 'center',
  },
  subtitle: {
    textAlign: 'center',
    marginBottom: 12,
    color: '#555',
  },
  note: {
    textAlign: 'center',
    marginBottom: 20,
    color: '#444',
    fontSize: 13,
  },
  buttonRow: {
    marginVertical: 8,
  },
  image: {
    width: '100%',
    height: 260,
    marginVertical: 16,
    borderRadius: 14,
  },
  resultBox: {
    marginTop: 18,
    padding: 16,
    backgroundColor: '#e6ffe6',
    borderRadius: 12,
  },
  resultText: {
    fontSize: 16,
    marginBottom: 6,
  },
});
